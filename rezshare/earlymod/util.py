
import os
import json
import stat
import shutil
from subprocess import check_output


def git_build_clone(url, branch, tag, callbacks=None):
    """
    This can be called multiple times during build, and will reuse previous
    clone data if exists.
    """
    if os.getenv("_GIT_CLONED_DATA"):
        data = json.loads(os.environ["_GIT_CLONED_DATA"])
        return data

    build_dir = os.path.join(os.getcwd(), "build")
    clonedir = os.path.join(build_dir, "__gitclonesrc__")
    if os.path.isdir(clonedir):
        clean(clonedir)

    # Clone and checkout specific commit/tag
    args = ["git", "clone", "--single-branch", "--branch", branch]
    args += [url, clonedir]
    check_output(args)
    git_checkout_tag(clonedir, tag)

    data = {
        "repo": clonedir,
        "branch": branch,
        "tag": tag,
        "authors": git_authors(clonedir),
    }
    # Additional callbacks that require git
    for callback in callbacks or []:
        callback(data)

    # Avoid repeating in each variation build
    os.environ["_GIT_CLONED_DATA"] = json.dumps(data)

    # Remove .git for tidy
    clean(os.path.join(clonedir, ".git"))

    return data


def git_checkout_tag(path, tag):
    check_output(["git", "checkout", tag], cwd=path)


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

    git_checkout_tag(path, tag)

    return tag


def git_authors(path):
    name_list = check_output(
        ["git", "shortlog", "-sn"],
        cwd=path
    ).decode()
    return [
        n.strip().split("\t", 1)[-1]
        for n in name_list.strip().split("\n")
    ]


def git_branch(path):
    return check_output(
        ["git", "branch", "--show-current"],
        universal_newlines=True,
        cwd=path,
    ).strip()


def clean(root):
    def del_rw(action, name, exc):
        # handling read-only files, e.g. in .git
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)
    shutil.rmtree(root, onerror=del_rw)
