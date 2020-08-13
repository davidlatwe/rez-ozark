early = globals()["early"]  # lint helper


name = "allzpark"

uuid = "repository.allzpark"

description = "Package-based application launcher for VFX and games " \
              "production"


@early()
def version():
    import subprocess

    version_str = subprocess.check_output(["python", "setup.py", "--version"],
                                          # Ensure strings are returned from both Python 2 and 3
                                          universal_newlines=True,
                                          ).strip()
    branch_name = subprocess.check_output(["git", "branch", "--show-current"],
                                          # Ensure strings are returned from both Python 2 and 3
                                          universal_newlines=True,
                                          ).strip()

    major, minor, patch = version_str.split(".")
    return "%s.%s-%s.%s" % (major, minor, branch_name, patch)


@early()
def authors():
    from subprocess import check_output

    name_list = check_output(["git", "shortlog", "-sn"]).strip().decode()
    contributors = [n.strip().split("\t", 1)[-1]
                    for n in name_list.split("\n")]

    return contributors


requires = [
    "rez",
    "Qt.py",
    "python",
]


build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/lib")
