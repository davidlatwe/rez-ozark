
# 1. Install Rez from source
# 2. Deploy

import os
import subprocess


root = os.path.dirname(__file__)

packages = [

    {
        "name": "os",
        "command": {
            "args": ["rez-bind", "--release", "os"],
            "cwd": root,
        },
    },

    {
        "name": "rez",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "rezpkg"),
        },
    },

    {
        "name": "default",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "_base", "default"),
        },
    },

    {
        "name": "miniconda",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "miniconda", "miniconda"),
        },
    },

    {
        "name": "python-3.6",
        "command": {
            "args": ["rez-release", "--version=3.6"],
            "cwd": os.path.join(root, "miniconda", "python"),
        },
    },

    {
        "name": "gitz",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "gitz"),
        },
    },

    {
        "name": "pipz",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "pipz"),
        },
    },

    {
        "name": "PySide2",
        "command": {
            "args": ["rez-env", "pipz", "--", "install", "PySide2",
                     "--release", "--yes"],
            "cwd": root,
        },
    },

    {
        "name": "PyQt5",
        "command": {
            "args": ["rez-env", "pipz", "--", "install", "PyQt5",
                     "--release", "--yes"],
            "cwd": root,
        },
    },

    {
        "name": "Qt.py",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "Qt.rez"),
        },
    },

    {
        "name": "rich",
        "command": {
            "args": ["rez-env", "pipz", "--", "install", "rich",
                     "--release", "--yes"],
            "cwd": root,
        },
    },

    {
        "name": "environs",
        "command": {
            "args": ["rez-env", "pipz", "--", "install", "environs",
                     "--release", "--yes"],
            "cwd": root,
        },
    },

    {
        "name": "site",
        "command": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "_base", "site"),
        },
    },

]


def release(package):
    print("Releasing package %s ..." % package["name"])
    subprocess.check_output(**package["command"])


if __name__ == "__main__":
    for pkg in packages:
        release(pkg)
