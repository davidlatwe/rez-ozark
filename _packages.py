
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
            "cwd": os.path.join(root, "default"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "default"),
        },
    },

    {
        "name": "miniconda",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "miniconda"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "miniconda"),
        },
    },

    {
        "name": "python-3.6",
        "install": {
            "args": ["rez-build", "--install", "--version=3.6"],
            "cwd": os.path.join(root, "python"),
        },
        "release": {
            "args": ["rez-release", "--version=3.6"],
            "cwd": os.path.join(root, "python"),
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
        "name": "rezcore",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "rezcore"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "rezcore"),
        },
    },

    {
        "name": "rezutil",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "rezutil"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "rezutil"),
        },
    },

    {
        "name": "pyidle",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "pyidle"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "pyidle"),
        },
    },

    {
        "name": "localz",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "localz"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "localz"),
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
            "cwd": os.path.join(root, "Qt.py"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "Qt.py"),
        },
    },

    {
        "name": "Pillow",
        "install": {
            "args": ["rez-env", "pipz", "--", "install", "Pillow", "--yes"],
            "cwd": root,
        },
        "release": {
            "args": ["rez-env", "pipz", "--", "install", "Pillow", "--yes",
                     "--release"],
            "cwd": root,
        },
    },

    {
        "name": "identicon",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "identicon"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "identicon"),
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

    {
        "name": "allzpark",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "allzpark"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "allzpark"),
        },
    },

    {
        "name": "ozark",
        "install": {
            "args": ["rez-build", "--install"],
            "cwd": os.path.join(root, "ozark"),
        },
        "release": {
            "args": ["rez-release"],
            "cwd": os.path.join(root, "ozark"),
        },
    },

]


def deploy(package, release=None):
    print("Releasing package %s ..." % package["name"])
    operation = "release" if release else "install"
    assert subprocess.check_call(**package[operation]) == 0
