
early = globals()["early"]


name = "python"

description = "System python"


@early()
def version():
    import sys
    return "system.%d.%d.%d" % sys.version_info[:3]


variants = [
    ["platform-*"],
]

build_command = False


def commands():
    import os
    import sys
    env = globals()["env"]

    env.PATH.prepend(os.path.dirname(sys.executable))
