
name = "house"

uuid = "studio.house"

version = "0.1.0"

description = "Studio/site-wide house production environment entry"

build_command = "python {root}/rezbuild.py {install}"


requires = [
    "python",
    "pymongo",
    "environs",
    # (NOTE) Disable 'rich' for now until rez-pipz#30 gets resolved
    # "rich",
    "ozark",
]

variants = [
    ["default"],
]


def pre_commands():
    # Parse environment setup from .env via `environs`
    # `AVALON_DEADLINE`
    # `AVALON_MONGODB`
    # ...
    pass


def commands():
    env = globals()["env"]  # linter help

    env.REZ_RELEASE_SHOWS_PATH = "~/rez/shows"

    # May add some welcome message here. With `rich`
