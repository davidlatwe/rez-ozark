
import os
early = globals()["early"]
__localzsrc = os.getcwd() + "src"


name = "localz"

uuid = "repository.localz"

description = "Package localisation for Rez"


@early()
def version():
    src_pkg = os.path.join(__localzsrc, "package.py")

    _globals = globals().copy()
    with open(src_pkg, "r") as pkg:
        pkg_source = "".join(pkg.readlines())
        exec(pkg_source, _globals)

    return _globals.get("version", "unknown")


@early()
def authors():
    import subprocess

    name_list = subprocess.check_output(
        ["git", "shortlog", "-sn"],
        universal_newlines=True,
        cwd=__localzsrc,
    ).strip()
    contributors = [n.strip().split("\t", 1)[-1]
                    for n in name_list.split("\n")]

    return contributors


tools = [
    "listen",
    "localise",
    "localize",
]


requires = [
    "python-2.7+,<4",
    "rez-2.29+",
]

build_command = "python -m rezutil build {root}src"
private_build_requires = ["rezutil-1"]


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
