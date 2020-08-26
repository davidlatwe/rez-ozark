
early = globals()["early"]  # lint helper


name = "allzpark"

uuid = "repository.allzpark"

description = "Package-based application launcher for VFX and games " \
              "production"


@early()
def __payload():
    from earlymod import util
    return util.git_build_clone(
        url="https://github.com/davidlatwe/allzpark.git",
        branch="dev",
    )


@early()
def version():
    import subprocess
    data = globals()["this"].__payload

    version_str = subprocess.check_output(
        ["python", "setup.py", "--version"],
        # Ensure strings are returned from both Python 2 and 3
        universal_newlines=True,
        cwd=data["repo"],
    ).strip()
    branch_name = subprocess.check_output(
        ["git", "branch", "--show-current"],
        universal_newlines=True,
        cwd=data["repo"],
    ).strip()

    major, minor, patch = version_str.split(".")
    return "%s-%s.%s.%s" % (branch_name, major, minor, patch)


@early()
def authors():
    from earlymod import util
    data = globals()["this"].__payload
    return util.git_authors(data["repo"])


tools = [
    "allzpark",
    "park",  # alias of `allzpark`
]

requires = [
    "rez",
    "Qt.py",
    "python",
]


private_build_requires = ["rezutil-1"]


@early()
def build_command():
    import os
    data = globals()["this"].__payload
    os.environ["_GIT_CLONED_SRC_PATH"] = data["repo"]
    return "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    alias = globals()["alias"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib")

    alias("park", "allzpark")
