
import os


""" Optional release path from environment

If following environment var presented, will *APPEND* into `packages_path`.
These environ vars can be provided by packages' `commands`.

"""
__OPT_RELEASE_KEYS = [
    # pipeline modules, internal tools.
    "REZ_OPT_RELEASE_INT_PATH",
    # DCC Apps, plugins, other third party, external stuff.
    "REZ_OPT_RELEASE_EXT_PATH",
]


# Rez's default package path excluded
local_packages_path = "~/rez/packages/install"
release_packages_path = "~/rez/packages/release"
packages_path = [
    local_packages_path,
    release_packages_path,
]
# *Append* additional release path
for key in __OPT_RELEASE_KEYS:
    if os.getenv(key):
        packages_path.append(os.environ[key])


package_preprocess_mode = "before"
# "before": Package's preprocess is executed before the global preprocess
# "after": Package's preprocess is executed after the global preprocess
# "override": Package's preprocess completely overrides the global preprocess


def package_preprocess_function(this, data):
    from rez.utils.formatting import PackageRequest

    # Must have variant
    #

    if this.name != "default" and not this.variants:
        # Add "default" if no variant
        data["variants"] = [["default"]]

    # Replacing package requirements
    #

    REQUIREMENT_MAP = {
        # Example
        "installing_package_name": {
            "required_request_string": "replacement_request_string",
        },

    }
    if this.name in REQUIREMENT_MAP:

        remapped_requires = list()

        map_ = REQUIREMENT_MAP[this.name]
        for package in this.requires:

            if str(package) in map_:
                package = PackageRequest(map_[str(package)])

            elif package.name in map_:
                package = PackageRequest(map_[package.name])

            remapped_requires.append(package)

        data["requires"] = remapped_requires
