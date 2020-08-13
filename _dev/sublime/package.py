
name = "sublime"

uuid = "repository.dev.sublime"

version = "latest"

description = "A sophisticated text editor for code, markup and prose"

authors = ["Sublime HQ Pty Ltd"]

tools = [
    "sublime",
]

variants = [
    ["platform-*"],
]

build_command = False


def commands():
    system = globals()["system"]
    env = globals()["env"]
    alias = globals()["alias"]

    if system.platform == "windows":
        raise NotImplementedError

    elif system.platform == "osx":
        env.PATH.prepend("/Applications/PyCharm CE.app/Contents/MacOS")
        alias("sublime", "Sublime Text")

    elif system.platform == "linux":
        raise NotImplementedError

    else:
        print("Unknown platform: %s" % system.platform)
