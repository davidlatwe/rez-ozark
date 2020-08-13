
import os
import subprocess


root = os.path.dirname(__file__)

packages = [

    {
        "name": "os",
        "install": {
            "args": ["rez-bind", "os"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-bind", "--release", "os"],
            "cwd": root,
        },
    },

    {
        "name": "default",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "_base", "default"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "_base", "default"),
        },
    },

    {
        "name": "miniconda",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "miniconda", "miniconda"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "miniconda", "miniconda"),
        },
    },

    {
        "name": "python-3.6",
        "install": {
            "args": ["rez-build", "--install", "--version=3.6"],
            "cwd": os.path.join(root, "miniconda", "python"),
        },
        "release": {
            "args": ["rez-release", "--version=3.6"],
            "cwd": os.path.join(root, "miniconda", "python"),
        },
    },

    {
        "name": "rez",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "rezpkg"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "rezpkg"),
        },
    },

    {
        "name": "gitz",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "gitz"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "gitz"),
        },
    },

    {
        "name": "pipz",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "pipz"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "pipz"),
        },
    },

    {
        "name": "PySide2",
        "install": {
            "args": ["rez-env", "pipz", "--", "install", "PySide2", "--yes"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-env", "pipz", "--", "install", "PySide2", "--yes",
                     "--release"],
            "cwd": root,
        },
    },

    {
        "name": "PyQt5",
        "install": {
            "args": ["rez-env", "pipz", "--", "install", "PyQt5", "--yes"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-env", "pipz", "--", "install", "PyQt5", "--yes",
                     "--release"],
            "cwd": root,
        },
    },

    {
        "name": "Qt.py",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "Qt.rez"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "Qt.rez"),
        },
    },

    {
        "name": "rezgui",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "rezgui"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "rezgui"),
        },
    },

    # (NOTE) Disable 'rich' for now until rez-pipz#30 gets resolved
    # {
    #     "name": "rich",
    #     "install": {
    #         "args": ["rez-env", "pipz", "--", "install", "rich", "--yes"],
    #         "cwd": root,
    #     },
    #     "release": {
    #         "args": ["rez-env", "pipz", "--", "install", "rich", "--yes",
    #                  "--release"],
    #         "cwd": root,
    #     },
    # },

    {
        "name": "environs",
        "install": {
            "args": ["rez-env", "pipz", "--", "install", "environs", "--yes"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-env", "pipz", "--", "install", "environs", "--yes",
                     "--release"],
            "cwd": root,
        },
    },

    {
        "name": "pymongo",
        "install": {
            "args": ["rez-env", "pipz", "--", "install", "pymongo", "--yes"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-env", "pipz", "--", "install", "pymongo", "--yes",
                     "--release"],
            "cwd": root,
        },
    },

    {
        "name": "house",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "_base", "house"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "_base", "house"),
        },
    },

]


def deploy(package, release=None):
    print("Releasing package %s ..." % package["name"])
    operation = "release" if release else "install"
    assert subprocess.check_call(**package[operation]) == 0
