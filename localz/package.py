
import os
early = globals()["early"]


name = "localz"

uuid = "repository.localz"

description = "Package localisation for Rez"


@early()
def __payload():
    from earlymod import util
    return util.git_build_clone(
        url="https://github.com/mottosso/rez-localz.git",
        branch="master",
        tag="0f7a472b25f0a333ad080bbc42a6140249cb8838",
    )


@early()
def version():
    data = globals()["this"].__payload
    src_pkg = os.path.join(data["repo"], "package.py")

    _globals = globals().copy()
    with open(src_pkg, "r") as pkg:
        pkg_source = "".join(pkg.readlines())
        exec(pkg_source, _globals)

    return _globals["version"]


@early()
def authors():
    data = globals()["this"].__payload
    return data["authors"]


tools = [
    "listen",
    "localise",
    "localize",
]


requires = [
    "python-2.7+,<4",
    "rez-2.29+",
]


private_build_requires = ["rezutil-1"]


@early()
def build_command():
    data = globals()["this"].__payload
    return "python -m rezutil build {root}".format(
        root=data["repo"],
    )


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
