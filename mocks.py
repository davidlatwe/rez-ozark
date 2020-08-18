
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
            "house",
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
            "house",
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
            "house",
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
            "house",
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
            "house",
        ],
        "tools": [
            "blender",
        ]
    },

]


def mock(name, versions, requires, tools):
    for version in versions:

        args = [
            "rez-build",
            "--install",
            "--name",
            name,
            "--version",
            version,
            "--requires",
        ] + requires + [
            "--tools"
        ] + tools

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
