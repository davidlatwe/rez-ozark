
import os
early = globals()["early"]  # lint helper
__allzparksrc = os.getcwd() + "src"


name = "allzpark"

uuid = "repository.allzpark"

description = "Package-based application launcher for VFX and games " \
              "production"


@early()
def version():
    import subprocess

    version_str = subprocess.check_output(
        ["python", "setup.py", "--version"],
        # Ensure strings are returned from both Python 2 and 3
        universal_newlines=True,
        cwd=__allzparksrc,
    ).strip()
    branch_name = subprocess.check_output(
        ["git", "branch", "--show-current"],
        universal_newlines=True,
        cwd=__allzparksrc,
    ).strip()

    major, minor, patch = version_str.split(".")
    return "%s.%s-%s.%s" % (major, minor, branch_name, patch)


@early()
def authors():
    import subprocess

    name_list = subprocess.check_output(
        ["git", "shortlog", "-sn"],
        universal_newlines=True,
        cwd=__allzparksrc,
    ).strip()
    contributors = [n.strip().split("\t", 1)[-1]
                    for n in name_list.split("\n")]

    return contributors


tools = [
    "allzpark",
]

requires = [
    "rez",
    "Qt.py",
    "python",
]


build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib")
