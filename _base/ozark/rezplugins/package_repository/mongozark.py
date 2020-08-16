
from rez.vendor.version.requirement import VersionedObject
from rez.package_repository import PackageRepository
from rez.package_resources import (
    PackageFamilyResource,
    VariantResourceHelper,
    PackageResourceHelper,
    package_pod_schema,
    package_release_keys,
    package_build_only_keys,
)
from rez.exceptions import (
    PackageRepositoryError,
    PackageMetadataError,
    RezSystemError,
)
from rez.utils.formatting import is_valid_package_name
from rez.utils.resources import cached_property
from rez.config import config
from rez.backport.lru_cache import lru_cache
from rez.vendor.six import six

from rez.utils.sourcecode import SourceCode
from rez.vendor.version.version import Version

import os
import time
import socket
import getpass
import datetime

from pymongo import MongoClient
from montydb import MontyClient, configure as monty_config

basestring = six.string_types[0]


class PackageDefinitionFileMissing(PackageMetadataError):
    pass


def package_document(name, version, package_dict):
    return {
        "name": name,
        "version": version,
        "package": package_dict,
        "date": datetime.datetime.now(),
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
    }


def _encode(obj):

    if isinstance(obj, SourceCode):
        # Reference: SourceCode.__getstate__
        return {
            "::rez:sourcecode::": dict(
                source=obj.source,
                filepath=obj.filepath,
                funcname=obj.funcname,
                eval_as_function=obj.eval_as_function,
                decorators=obj.decorators,
            )
        }

    if isinstance(obj, Version):
        return {
            "::rez:version::": dict(
                version=str(obj),
            )
        }

    return obj


def package_to_dict(package):
    return {
        k: _encode(v)
        for k, v in package.items()
        if v is not None
    }


def _decode(obj):

    if not isinstance(obj, dict):
        return obj

    if "::rez:sourcecode::" in obj:
        value = obj["::rez:sourcecode::"]

        source_code = SourceCode()
        # Reference: SourceCode.__setstate__
        source_code.source = value["source"]
        source_code.filepath = value["filepath"]
        source_code.funcname = value["funcname"]
        source_code.eval_as_function = value["eval_as_function"]
        source_code.decorators = value["decorators"]

        return source_code

    if "::rez:version::" in obj:
        value = obj["::rez:version::"]

        return Version(value["version"])

    return obj


def package_from_dict(package):
    return {
        k: _decode(v)
        for k, v in package.items()
        if v is not None
    }


# ------------------------------------------------------------------------------
# resources
# ------------------------------------------------------------------------------


class MongozarkPackageFamilyResource(PackageFamilyResource):
    key = "mongozark.family"
    repository_type = "mongozark"

    def _uri(self):
        return "%s@%s" % (self.name, self.location)

    def get_last_release_time(self):
        data = self._repository.collection.find_one(
            {"name": self.name},
            projection={"date": True},
            sort=[("date", -1)],
        )

        if data is None or "date" not in data:
            return 0
        else:
            return time.mktime(data["date"].timetuple())

    def iter_packages(self):
        for data in self._repository.collection.find(
            {"name": self.name},
            projection={"version": True},
        ):

            package = self._repository.get_resource(
                MongozarkPackageResource.key,
                location=self.location,
                name=self.name,
                version=data["version"])

            yield package


class MongozarkPackageResource(PackageResourceHelper):
    key = "mongozark.package"
    variant_key = "mongozark.variant"
    repository_type = "mongozark"
    schema = package_pod_schema

    def _uri(self):
        obj = VersionedObject.construct(self.name, self.version)
        return "mongozark@%s->%s" % (self.location, str(obj))

    @cached_property
    def parent(self):
        family = self._repository.get_resource(
            MongozarkPackageFamilyResource.key,
            location=self.location,
            name=self.name)
        return family

    def state_handle(self):
        # Not applicable to mongodb repository type
        #
        # This is used for resolve caching. For example, in the 'filesystem'
        # repository type, the 'state' is the last modified date of the file
        # associated with the variant (perhaps a package.py). Which don't fit
        # for repository that backed with database.

        return None

    def iter_variants(self):
        indexes = [None]  # No variant needed/allowed in mongozark

        for index in indexes:
            variant = self._repository.get_resource(
                self.variant_key,
                location=self.location,
                name=self.name,
                version=self.get("version"),
                index=index)

            yield variant

    @property
    def base(self):
        return None  # mongodb resource doesn't have 'base' path

    def _load(self):
        data = self._repository.collection.find_one(
            {
                "name": self.name,
                "version": self.get("version"),
            },
            projection={"package": True}
        )

        if data is None:
            raise PackageDefinitionFileMissing(
                "Missing package definition file: %r" % self)

        return package_from_dict(data["package"])


class MongozarkVariantResource(VariantResourceHelper):
    key = "mongozark.variant"
    repository_type = "mongozark"

    @cached_property
    def parent(self):
        package = self._repository.get_resource(
            MongozarkPackageResource.key,
            location=self.location,
            name=self.name,
            version=self.get("version"))
        return package


def is_montydb_uri(uri):
    return uri.startswith(monty_config.URI_SCHEME_PREFIX)


class MongozarkPackageRepository(PackageRepository):
    """
    """

    @classmethod
    def name(cls):
        return "mongozark"

    def __init__(self, location, resource_pool):
        """Create a mongo package repository.

        Args:
         location (str): Path containing the package repository.

        """
        uri_key, database, collection = location.split(".", 3)

        settings = config.plugins.package_repository.mongozark
        uri = getattr(settings.uri, uri_key, None)

        if uri is None:
            raise PackageRepositoryError(
                "URI key '%s' not found in "
                "'config.plugins.package_repository.mongozark.uri'." % uri_key)

        if is_montydb_uri(uri):
            client = MontyClient(uri)
        else:
            client = MongoClient(uri)

        db = client[database]
        self.collection = db[collection]

        super(MongozarkPackageRepository, self).__init__(location,
                                                         resource_pool)

        self.register_resource(MongozarkPackageFamilyResource)
        self.register_resource(MongozarkVariantResource)
        self.register_resource(MongozarkPackageResource)

        self.get_families = lru_cache(maxsize=None)(self._get_families)
        self.get_family = lru_cache(maxsize=None)(self._get_family)
        self.get_packages = lru_cache(maxsize=None)(self._get_packages)
        self.get_variants = lru_cache(maxsize=None)(self._get_variants)

    def _uid(self):
        return self.name(), self.location

    def get_package_family(self, name):
        return self.get_family(name)

    def iter_package_families(self):
        for family in self.get_families():
            yield family

    def iter_packages(self, package_family_resource):
        for package in self.get_packages(package_family_resource):
            yield package

    def iter_variants(self, package_resource):
        for variant in self.get_variants(package_resource):
            yield variant

    def get_parent_package_family(self, package_resource):
        return package_resource.parent

    def get_parent_package(self, variant_resource):
        return variant_resource.parent

    def get_variant_state_handle(self, variant_resource):
        # Not applicable to mongodb repository type, leave it as-is.
        return None

    def get_last_release_time(self, package_family_resource):
        return package_family_resource.get_last_release_time()

    def install_variant(self, variant_resource, dry_run=False, overrides=None):
        overrides = overrides or {}

        # Name and version overrides are a special case - they change the
        # destination variant to be created/replaced.
        #
        variant_name = variant_resource.name
        variant_version = variant_resource.version

        if "name" in overrides:
            variant_name = overrides["name"]
            if variant_name is self.remove:
                raise PackageRepositoryError(
                    "Cannot remove package attribute 'name'")

        if "version" in overrides:
            ver = overrides["version"]
            if ver is self.remove:
                raise PackageRepositoryError(
                    "Cannot remove package attribute 'version'")

            if isinstance(ver, basestring):
                ver = Version(ver)
                overrides = overrides.copy()
                overrides["version"] = ver

            variant_version = ver

        # cannot install over one's self, just return existing variant
        if variant_resource._repository is self and \
                variant_name == variant_resource.name and \
                variant_version == variant_resource.version:
            return variant_resource

        # install the variant
        variant = self._create_variant(variant_resource,
                                       dry_run=dry_run,
                                       overrides=overrides)
        return variant

    def clear_caches(self):
        super(MongozarkPackageRepository, self).clear_caches()
        self.get_families.cache_clear()
        self.get_family.cache_clear()
        self.get_packages.cache_clear()

    def get_package_payload_path(self, package_name, package_version=None):
        # (NOTE) We wouldn't need this,
        #   but the local build process need a place to write
        #   out `build.rxt` file, so we set the path to the
        #   build dir.
        path = os.path.join("build", ".install")
        return path

    def _get_families(self):
        families = []

        for name in self.collection.distinct("name"):
            family = self.get_resource(
                MongozarkPackageFamilyResource.key,
                location=self.location,
                name=name)

            families.append(family)

        return families

    def _get_family(self, name):
        is_valid_package_name(name, raise_error=True)

        pkg = self.collection.find_one({"name": name}, projection={"_id": True})
        if pkg is not None:

            family = self.get_resource(
                MongozarkPackageFamilyResource.key,
                location=self.location,
                name=name
            )

            return family

    def _get_packages(self, package_family_resource):
        return [x for x in package_family_resource.iter_packages()]

    def _get_variants(self, package_resource):
        return [x for x in package_resource.iter_variants()]

    def _create_variant(self, variant, dry_run=False, overrides=None):
        # special case overrides
        variant_name = overrides.get("name") or variant.name
        variant_version = overrides.get("version") or variant.version

        overrides = (overrides or {}).copy()
        overrides.pop("name", None)
        overrides.pop("version", None)

        # Need to treat 'config' as special case. In validated data, this is
        # converted to a Config object. We need it as the raw dict that you'd
        # see in a package.py.
        #
        def _get_package_data(pkg):
            data = pkg.validated_data()
            if hasattr(pkg, "_data"):
                raw_data = pkg._data
            else:
                raw_data = pkg.resource._data

            raw_config_data = raw_data.get("config")
            data.pop("config", None)

            if raw_config_data:
                data["config"] = raw_config_data

            return data

        def _remove_build_keys(obj):
            for key in package_build_only_keys:
                obj.pop(key, None)

        package_data = _get_package_data(variant.parent)
        package_data.pop("variants", None)
        package_data["name"] = variant_name
        if variant_version:
            package_data["version"] = variant_version

        _remove_build_keys(package_data)

        installed_variant_index = None

        if dry_run:
            return None

        # a little data massaging is needed
        package_data.pop("base", None)

        # Apply overrides
        for key, value in overrides.items():
            if value is self.remove:
                package_data.pop(key, None)
            else:
                package_data[key] = value

        # timestamp defaults to now if not specified
        if not package_data.get("timestamp"):
            package_data["timestamp"] = int(time.time())

        # format version is always set
        package_data["format_version"] = 2  # Late binding functions added

        # Upsert to database
        version_string = str(package_data["version"])

        document = package_document(package_data["name"],
                                    version_string,
                                    package_to_dict(package_data))
        filter_ = {
            "name": package_data["name"],
            "version": version_string,
        }
        self.collection.update_one(filter_, {"$set": document}, upsert=True)

        # load new variant
        new_variant = None
        self.clear_caches()
        family = self.get_package_family(variant_name)

        if family:
            for package in self.iter_packages(family):
                if package.version == variant_version:
                    for variant_ in self.iter_variants(package):
                        if variant_.index == installed_variant_index:
                            new_variant = variant_
                            break
                elif new_variant:
                    break

        if not new_variant:
            raise RezSystemError("Internal failure - expected installed variant")

        return new_variant


def register_plugin():
    return MongozarkPackageRepository
