
import os
ModifyList = globals()["ModifyList"]


categories = [
    "_gitz",
    "_pipz",
    # there should be more ...
]

local_packages_path = "~/rez/packages/local-install"
release_packages_path = "~/rez/packages/local-release"
packages_path = ModifyList(
    prepend=[
        local_packages_path,
        release_packages_path,
    ] + [
        os.path.join(release_packages_path, category)
        for category in categories
    ]
)


def package_preprocess_function(this, data):
    import os
    from rez.config import config

    config_override = data.get("config", {})

    # Redirecting package release path
    #

    # davidlatwe/rez-gitz
    if data.get("gitz"):
        config_override["release_packages_path"] = os.path.join(
            config.release_packages_path, "_gitz"
        )

    # mottosso/rez-pipz
    if data.get("pipz"):
        # This change will be ignored if "--prefix" has set
        config_override["release_packages_path"] = os.path.join(
            config.release_packages_path, "_pipz"
        )

    data["config"] = config_override
