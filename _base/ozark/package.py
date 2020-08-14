
name = "ozark"

version = "0.1.0"

description = "Able to read from MongoDB"

authors = ["davidlatwe"]

requires = [
    "python",
    "pymongo",
    "allzpark",
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.ALLZPARK_CONFIG_FILE = "{root}/config/allzparkconfig.py"
    env.REZ_CONFIG_FILE.append("{root}/config/rezconfig.py")

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")


def post_commands():
    # print mongodb uri
    pass
