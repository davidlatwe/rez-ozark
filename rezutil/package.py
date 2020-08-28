
name = "rezutil"

version = "1.4.0"


# build with bez build system


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/python")
