
import os
early = globals()["early"]


name = "pipz"

uuid = "repository.pipz"

description = "Pip for Rez - Install any Python package from PyPI " \
              "as a Rez package"


@early()
def __payload():
    from earlymod import util
    return util.git_build_clone(
        url="https://github.com/davidlatwe/rez-pipz.git",
        branch="dev",
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
    "install",
    "search",
]


requires = [
    "python-2.7+,<4",
    "rez-2.29+",
]


@early()
def build_command():
    data = globals()["this"].__payload
    return " ".join([
        "python {root}/install.py ".format(root=data["repo"]),

        # Upon a new release of pip, wheel or setuptools,
        # this is what you edit
        "--pip=20.2b1",
        "--wheel=0.33.4",
        "--setuptools=41.0.1",
        "--packaging=19.0",

    ])


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
