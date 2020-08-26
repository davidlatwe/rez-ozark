
early = globals()["early"]  # lint helper


name = "allzpark"

uuid = "repository.allzpark"

description = "Package-based application launcher for VFX and games " \
              "production"


@early()
def __payload():
    from earlymod import util

    def patch(clonedir):
        import os
        import shutil
        # Copy into "{root}/python"
        shutil.copytree(os.path.join(clonedir, "allzpark"),
                        os.path.join(clonedir, "python", "allzpark"))
        # Add into "{root}/bin"
        for dirname in ["bin"]:
            dir_src = os.path.join(os.getcwd(), dirname)
            dir_dst = os.path.join(clonedir, dirname)
            shutil.copytree(dir_src, dir_dst)

    return util.git_build_clone(
        url="https://github.com/davidlatwe/allzpark.git",
        branch="dev",
        callback=patch,
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
    sep = ",/"
    return "python -m rezutil build {root} --ignore {ignore} --quiet".format(
        root=data["repo"],
        ignore=sep.join(item for item in os.listdir(data["repo"])
                        if item not in ["python", "bin"])
    )


def commands():
    env = globals()["env"]
    alias = globals()["alias"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")

    alias("park", "allzpark")
