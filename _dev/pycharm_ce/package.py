
name = "pycharm"

uuid = "repository.dev.pycharm"

version = "latest.CE"

description = "The Python IDE for Professional Developers"

authors = ["JetBrains"]

tools = [
    "pycharm",
    "charm",
]

variants = [
    ["platform-*"],
]

build_command = "python {root}/rezbuild.py {install}"


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

    env.PATH.prepend("{root}/bin")
