
name = "pycharm"

uuid = "repository.dev.pycharm"

version = "latest.CE"

description = "The Python IDE for Professional Developers"

authors = ["JetBrains"]

tools = [
    "pycharm",
]

variants = [
    ["platform-*"],
]

build_command = False


def commands():
    system = globals()["system"]
    env = globals()["env"]

    if system.platform == "windows":
        raise NotImplementedError
    elif system.platform == "osx":
        env.PATH.prepend("/Applications/PyCharm CE.app/Contents/MacOS")
    elif system.platform == "linux":
        raise NotImplementedError
    else:
        print("Unknown platform: %s" % system.platform)
