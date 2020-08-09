
name = "site"

uuid = "studio.site"

version = "0.1.0"

description = "Studio/site-wide environment entry"

authors = ["davidlatwe"]

build_command = "python {root}/rezbuild.py {install}"


requires = [
    "python",
    "environs",
    # (NOTE) Disable 'rich' for now until rez-pipz#30 gets resolved
    # "rich",
]

variants = [
    ["default"],
]


def commands():
    env = globals()["env"]  # linter help
    env.REZ_CONFIG_FILE.append("{root}/payload/rezconfig.py")

    # Parse environment setup from .env via `environs`
    # `SITE_PACKAGES_RELEASE_PATH`
    # `AVALON_DEADLINE`
    # `AVALON_MONGODB`
    # ...

    # May add some welcome message here. With `rich`
