early = globals()["early"]

name = "Qt.py"

uuid = "repository.Qt.py"


@early()
def __latest():
    import os
    import json
    import shutil
    import tempfile
    from subprocess import check_output, CalledProcessError

    if os.getenv("GIT_CLONED"):
        # Reuse data from previous clone
        data = json.loads(os.environ["GIT_CLONED"])
        return data

    url = "https://github.com/mottosso/Qt.py.git"

    tmpdir = tempfile.mkdtemp()
    tempdir = os.path.join(tmpdir, "Qt.py")
    try:
        check_output(["git", "clone", "--single-branch", url, tempdir])
        check_output(["git", "fetch", "--tags"], cwd=tempdir)
        commit = check_output(["git", "rev-list", "--tags", "--max-count=1"],
                              cwd=tempdir).strip().decode()
        tag = check_output(["git", "describe", "--tags", commit],
                           cwd=tempdir).strip().decode()
        check_output(["git", "checkout", tag], cwd=tempdir)

    except CalledProcessError:
        shutil.rmtree(tmpdir)
        raise

    data = {
        "temp": tmpdir,
        "repo": tempdir,
        "tag": tag,
    }
    # Avoid repeating in each variation build
    os.environ["GIT_CLONED"] = json.dumps(data)

    return data


@early()
def version():
    this = globals()["this"]
    return this.__latest["tag"]


description = "Minimal Python 2 & 3 shim around all Qt bindings - "\
              "PySide, PySide2, PyQt4 and PyQt5."


@early()
def authors():
    from subprocess import check_output

    this = globals()["this"]
    repo = this.__latest["repo"]

    name_list = check_output(["git", "shortlog", "-sn"],
                             cwd=repo).strip().decode()
    contributors = [n.strip().split("\t", 1)[-1]
                    for n in name_list.split("\n")]
    contributors.append("davidlatwe")

    return contributors


def __has_package(pkg_request):
    from rez.packages import get_latest_package_from_string
    return get_latest_package_from_string(pkg_request)


@early()
def variants():
    import os
    import shutil

    bindings = [
        "PyQt5",
        "PySide2",
        "PyQt4",
        "PySide",
    ]
    variants_ = [
        [binding] for binding in bindings if __has_package(binding)
    ]
    if not variants_:
        # cleanup
        this = globals()["this"]
        shutil.rmtree(this.__latest["temp"])

        raise Exception("No Qt binding package found.")

    os.environ["REZ_BUILD_VARIANT_COUNT"] = str(len(variants_))

    return variants_


# build_requires = ["python-3"]  # For author name (unicode)

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/payload")
