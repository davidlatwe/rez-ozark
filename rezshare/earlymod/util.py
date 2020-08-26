
import os
import json
import stat
import shutil
from subprocess import check_output


def git_build_clone(url, branch=None, checkout_latest_tag=False):
    """
    This can be called multiple times during build, and will reuse previous
    clone data if exists.
    """
    if os.getenv("GIT_CLONED"):
        data = json.loads(os.environ["GIT_CLONED"])
        return data

    build_dir = os.path.join(os.getcwd(), "build")
    clonedir = os.path.join(build_dir, "__gitclonesrc__")
    if os.path.isdir(clonedir):
        clean(clonedir)

    args = ["git", "clone", "--single-branch"]
    if branch:
        args += ["--branch", branch]

    args += [url, clonedir]
    check_output(args)

    # no read-only, for later cleanup
    for base, dirs, files in os.walk(os.path.join(clonedir, ".git")):
        for file in files:
            os.chmod(os.path.join(base, file), stat.S_IWRITE)

    if checkout_latest_tag:
        tag = git_checkout_latest_tag(clonedir)
    else:
        tag = None

    data = {
        "repo": clonedir,
        "tag": tag,
    }
    # Avoid repeating in each variation build
    os.environ["GIT_CLONED"] = json.dumps(data)

    return data


def git_checkout_latest_tag(path):
    check_output(
        ["git", "fetch", "--tags"],
        cwd=path,
    )
    commit = check_output(
        ["git", "rev-list", "--tags", "--max-count=1"],
        universal_newlines=True,
        cwd=path,
    ).strip()
    tag = check_output(
        ["git", "describe", "--tags", commit],
        universal_newlines=True,
        cwd=path
    ).strip()
    check_output(["git", "checkout", tag], cwd=path)

    return tag


def git_authors(path):
    name_list = check_output(
        ["git", "shortlog", "-sn"],
        universal_newlines=True,
        cwd=path
    )
    return [
        n.strip().split("\t", 1)[-1]
        for n in name_list.strip().split("\n")
    ]


def clean(root):
    def del_rw(action, name, exc):
        # handling read-only files, e.g. in .git
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)
    shutil.rmtree(root, onerror=del_rw)
