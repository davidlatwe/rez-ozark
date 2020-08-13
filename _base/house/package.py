
include = globals()["include"]


name = "house"

uuid = "studio.house"

version = "0.1.0"

description = "Studio/site-wide house production environment entry"

requires = [
    "python",
    "pymongo",
    "python_dotenv",
    # (NOTE) Disable 'rich' for now until rez-pipz#30 gets resolved
    # "rich",
    # "ozark",
]

variants = [
    ["default"],
]


build_command = "python {root}/rezbuild.py {install}"


@include("libpkg")
def commands():
    import os
    libpkg = globals()["libpkg"]
    this = globals()["this"]
    env = globals()["env"]

    # Prepend env.PYTHONPATH into sys.path for later operation's
    # requirement
    libpkg.sys_path_prepend(env)

    # Parse environment setup from .env
    libpkg.load_dotenv(file=os.path.join(this.root, ".env"),
                       env=env)


def post_commands():
    # May add some welcome message here. With `rich`
    print("WELCOME TO THE PRODUCTION HOUSE !")
