
ModifyList = globals()["ModifyList"]

# REZ_LOCALIZED_PACKAGES_PATH
local_packages_path = "~/rez/packages/local-install"
release_packages_path = "~/rez/packages/local-release"
packages_path = ModifyList(
    prepend=[
        local_packages_path,
        release_packages_path,
    ]
)
