name = "rezutil"
version = "1.3.2"
requires = [
    "python-2.7+,<4",
]

_category = "int"
# build with bez build system


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/python")
