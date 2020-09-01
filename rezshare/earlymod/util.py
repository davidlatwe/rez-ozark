
import os
import sys
import json
import stat
import shutil
from subprocess import check_output


def git_payload(local, remote, callbacks=None):
    rez_dash_build = sys.argv[0].endswith("rez-build")
    rez_space_build = sys.argv[0].endswith("rez") and sys.argv[1] == "build"
    is_local = rez_dash_build or rez_space_build

    if local and is_local:
        return git_build_local(callbacks=callbacks, **local)
    else:
        return git_build_clone(callbacks=callbacks, **remote)


def git_build_local(path, tag, callbacks=None):
    if os.getenv("_GIT_REPO_DATA"):
        data = json.loads(os.environ["_GIT_REPO_DATA"])
        return data

    data = {
        "repo": path,
        "branch": git_branch(path),
        "tag": tag,
        "authors": git_authors(path),
    }
    # Additional callbacks that require git
    for callback in callbacks or []:
        callback(data)

    # Patch changelog
    patch_changelog(path)

    # Avoid repeating in each variation build
    os.environ["_GIT_REPO_DATA"] = json.dumps(data)

    return data


def git_build_clone(url, branch, tag, callbacks=None):
    """
    This can be called multiple times during build, and will reuse previous
    clone data if exists.
    """
    if os.getenv("_GIT_REPO_DATA"):
        data = json.loads(os.environ["_GIT_REPO_DATA"])
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

    # Patch changelog
    patch_changelog(clonedir)

    # Avoid repeating in each variation build
    os.environ["_GIT_REPO_DATA"] = json.dumps(data)

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


def patch_changelog(path):
    from rez.config import config
    from rez.build_process import BuildProcessHelper

    max_revisions = config.max_package_changelog_revisions
    args = ["git", "log"]
    if max_revisions:
        args.extend(["-n", str(max_revisions)])

    _changelog = check_output(args, cwd=path).decode()

    def git_get_changelog(previous_revision=None):
        if previous_revision is not None:
            # returns logs to last common ancestor
            prev_commit = "commit %s\n" % previous_revision["commit"]
            lines = list()
            for line in _changelog.split("\n"):
                if line == prev_commit:
                    break
                lines.append(line)

            return "\n".join(lines)
        else:
            return _changelog

    def get_changelog(self):
        previous_package = self.get_previous_release()
        if previous_package:
            previous_revision = previous_package.revision
        else:
            previous_revision = None

        return git_get_changelog(previous_revision)

    BuildProcessHelper.get_changelog = get_changelog
