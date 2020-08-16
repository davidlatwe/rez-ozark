
from rez.vendor.version.requirement import VersionedObject
from rez.package_repository import PackageRepository
from rez.package_resources import (
    PackageFamilyResource,
    VariantResourceHelper,
    PackageResourceHelper,
    package_pod_schema,
    package_release_keys,
)
from rez.exceptions import PackageMetadataError, ResourceError, RezSystemError
from rez.utils.formatting import is_valid_package_name
from rez.utils.resources import cached_property
from rez.config import config
from rez.backport.lru_cache import lru_cache

import time

from pymongo import MongoClient
# (TODO) Use montydb for local install
# from montydb import MontyClient


class PackageDefinitionFileMissing(PackageMetadataError):
    pass


# ------------------------------------------------------------------------------
# resources
# ------------------------------------------------------------------------------


"""Package Schema
{
    "_id": ObjectId,
    "name": "package_name",
    "mtime": datetime,
    "version": "0.1.0",
    "package": Package,
}
"""


class MongozarkPackageFamilyResource(PackageFamilyResource):
    key = "mongozark.family"
    repository_type = "mongozark"

    def _uri(self):
        return "%s@%s" % (self.name, self.location)

    def get_last_release_time(self):
        data = self._repository.packages.find_one(
            {"name": self.name},
            projection={"mtime": True},
            sort=[("mtime", -1)],
        )

        if data is None or "mtime" not in data:
            return 0
        else:
            return time.mktime(data["mtime"].timetuple())

    def iter_packages(self):
        for data in self._repository.packages.find(
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
        return "%s->%s" % (self.location, str(obj))

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
        data = self._repository.packages.find_one(
            {
                "name": self.name,
                "version": self.get("version"),
            },
            projection={"package": True}
        )

        if data is None:
            raise PackageDefinitionFileMissing(
                "Missing package definition file: %r" % self)

        return data["package"]


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
        settings = config.plugins.package_repository.mongozark
        database, collection = location.split(".", 2)

        client = MongoClient(settings.uri)
        db = client[database]

        self.packages = db[collection]

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
        raise NotImplementedError("Mongozark does not handle write operation.")

    def clear_caches(self):
        super(MongozarkPackageRepository, self).clear_caches()
        self.get_families.cache_clear()
        self.get_family.cache_clear()
        self.get_packages.cache_clear()

    def _get_families(self):
        families = []

        for name in self.packages.distinct("name"):
            family = self.get_resource(
                MongozarkPackageFamilyResource.key,
                location=self.location,
                name=name)

            families.append(family)

        return families

    def _get_family(self, name):
        is_valid_package_name(name, raise_error=True)

        pkg = self.packages.find_one({"name": name}, projection={"_id": True})
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


def register_plugin():
    return MongozarkPackageRepository
