name = "rezutil"
version = "1.4.0"
requires = [
    "python-2.7+,<4",
]

_category = "int"
# build with bez build system


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/python")
