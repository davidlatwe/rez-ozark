
name = "site"

uuid = "studio.site"

version = "0.1.0"

description = "Studio/site-wide environment setup"

authors = ["davidlatwe"]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]  # linter help
    env.REZ_CONFIG_FILE.append("{root}/payload/rezconfig.py")

    # May add some welcome message here.
