
name = "PyQt5"

description = "Python bindings for the Qt cross platform " \
              "application toolkit"

version = "5.15.0"

requires = [
    "PyQt5_sip-12.8+<13",
]

variants = [
    ["os-*", "python-*"],
]


private_build_requires = ["rezutil-1", "pipz"]
build_command = "python -m rezutil build {root} --use-pipz"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
