
early = globals()["early"]  # lint helper


name = "Qt.py"

uuid = "repository.Qt.py"

description = "Minimal Python 2 & 3 shim around all Qt bindings - " \
              "PySide, PySide2, PyQt4 and PyQt5."


@early()
def __payload():
    from earlymod import util
    return util.git_build_clone(
        url="https://github.com/mottosso/Qt.py.git",
        branch="master",
        tag="1.2.6",
    )


@early()
def version():
    data = globals()["this"].__payload
    return data["tag"]


@early()
def authors():
    data = globals()["this"].__payload
    return data["authors"]


@early()
def variants():
    from rez import packages

    bindings = [
        "PyQt5",
        "PySide2",
        "PyQt4",
        "PySide",
    ]
    variants_ = [
        [binding] for binding in bindings
        if packages.get_latest_package_from_string(binding)
    ]
    if not variants_:
        raise Exception("No Qt binding package found.")

    return variants_


private_build_requires = ["rezutil-1"]


@early()
def build_command():
    import os
    data = globals()["this"].__payload
    return "python -m rezutil build {root} --ignore {ignore}".format(
        root=data["repo"],
        ignore=",".join(item for item in os.listdir(data["repo"])
                        if item != "Qt.py")  # We only need Qt.py
    )


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}")
