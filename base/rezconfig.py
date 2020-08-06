

local_packages_path = "~/rez/install"
release_packages_path = "~/rez/release"

packages_path = [
    local_packages_path,  # locally installed, not yet deployed
    release_packages_path,
]

# "before": Package's preprocess is executed before the global preprocess
# "after": Package's preprocess is executed after the global preprocess
# "override": Package's preprocess completely overrides the global preprocess
package_preprocess_mode = "before"


def package_preprocess_function(this, data):
    from rez.config import config
    from rez.utils.formatting import PackageRequest
    import os

    config_override = data.get("config", {})

    # Redirecting package release path
    #

    if data.get("pipz"):  # mottosso/rez-pipz
        # This change will be ignored if "--prefix" has set

        # (TODO) Enable this after package categories being defined
        # config_override["release_packages_path"] = os.path.join(
        #     config.release_packages_path, "ext-pipz"
        # )
        pass

    data["config"] = config_override

    # Must have variant
    #
    if this.name != "default" and not this.variants:
        # Add "default" if no variant
        data["variants"] = [["default"]]

    # Modifying package requirements
    #

    REQUIREMENT_MAP = {

        "pipz": {
            "bleeding_rez": "rez",
        },

        "localz": {
            "bleeding_rez": "rez",
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
