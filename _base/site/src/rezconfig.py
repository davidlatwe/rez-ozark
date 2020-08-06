
ModifyList = globals()["ModifyList"]


categories = [
    "apps",
    # "projects",
    # "plugins",
    # there should be more ...
]


local_packages_path = "~/rez/site-install"
release_packages_path = "~/rez/site-release"

packages_path = ModifyList(prepend=[
    local_packages_path,  # locally installed, not yet deployed
    release_packages_path,
])
# in ~/.bash_profile
# # Prepend machine config
# #   use prepend so other configs from packages can have precedence
# #   Note: The last config in $REZ_CONFIG_FILE overrides previous
# export REZ_CONFIG_FILE=~/rez/rezconfig.py:$REZ_CONFIG_FILE


package_preprocess_mode = "before"
# "before": Package's preprocess is executed before the global preprocess
# "after": Package's preprocess is executed after the global preprocess
# "override": Package's preprocess completely overrides the global preprocess


def package_preprocess_function(this, data):
    from rez.config import config
    from rez.exceptions import InvalidPackageError
    from rez.utils.formatting import PackageRequest
    import os

    config_override = data.get("config", {})

    # Redirecting package release path
    #

    # davidlatwe/rez-gitz
    if data.get("gitz"):
        pass

    # mottosso/rez-pipz
    if data.get("pipz"):
        # This change will be ignored if "--prefix" has set
        pass

    # Site categorizing rules
    if data.get("category"):
        if data["category"] not in categories:
            raise InvalidPackageError("Invalid package category: %s"
                                      % data["category"])

        config_override["release_packages_path"] = os.path.join(
            config.release_packages_path, data["category"]
        )

    data["config"] = config_override

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
