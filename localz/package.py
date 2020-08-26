
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
    from earlymod import util
    data = globals()["this"].__payload
    return util.git_authors(data["repo"])


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
