
import os
import subprocess


root = os.path.dirname(__file__)

applications = [

    {
        "name": "maya",
        "versions": [
            "2018",
            "2020",
        ],
        "requires": [
        ],
        "tools": [
            "maya",
            "mayapy",
            "render",
        ]
    },

    {
        "name": "houdini",
        "versions": [
            "17.5.173",
            "18.0.416",
        ],
        "requires": [
        ],
        "tools": [
            "hython",
            "houdini",
        ]
    },

    {
        "name": "nuke",
        "versions": [
            "9",
            "10",
            "11",
        ],
        "requires": [
        ],
        "tools": [
            "nuke",
            "nukex",
        ]
    },

    {
        "name": "terminal",
        "versions": [
            "0",
        ],
        "requires": [
        ],
        "tools": [
            "terminal",
        ]
    },

    {
        "name": "blender",
        "versions": [
            "2.97",
            "2.98",
        ],
        "requires": [
        ],
        "tools": [
            "blender",
        ]
    },

]


def mock(name, versions, requires, tools):
    for version in versions:

        if requires:
            arg_requires = ["--requires"] + requires
        else:
            arg_requires = []

        if tools:
            arg_tools = ["--tools"] + tools
        else:
            arg_tools = []

        args = [
            "rez-build",
            "--install",
            "--name",
            name,
            "--version",
            version,
        ]
        args += arg_requires
        args += arg_tools

        subprocess.check_call(args, cwd=os.path.join(root, "mockapp"))


def mock_all():
    for app in applications:
        mock(**app)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Mock Applications")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Mock all pre-defined applications."
    )

    opt, unknown = parser.parse_known_args()

    if opt.all:
        mock_all()
