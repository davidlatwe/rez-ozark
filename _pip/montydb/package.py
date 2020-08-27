
name = "montydb"

description = "MongoDB's unofficial Python implementation."

version = "2.1.1"

requires = []

variants = [
    ["python-3"],
]


private_build_requires = ["rezutil-1", "pipz"]
build_command = "python -m rezutil build {root} --use-pipz"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
