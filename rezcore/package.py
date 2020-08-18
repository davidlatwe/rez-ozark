
name = "rezcore"

description = "Find and enter Rez's virtual env, use with caution."

version = "0"

build_command = False


def commands():
    import os
    import rez
    import platform
    env = globals()["env"]

    rez_module = rez.__path__[0]  # $REZ_USED

    if platform.system() == "Windows":
        bin_dir = "Scripts"
        feature = {"activate", "rez", "pip.exe", "python.exe"}
    else:
        bin_dir = "bin"
        feature = {"activate", "rez", "pip", "python"}

    # Look up for bin dir
    def up(path):
        return os.path.dirname(path)

    current = os.path.dirname(rez_module)
    location = None
    while True:
        if bin_dir not in os.listdir(current):
            parent_dir = up(current)
            if current == parent_dir:
                break  # reached to root
            current = parent_dir
        else:
            found = os.path.join(current, bin_dir)
            content = set(os.listdir(found))
            if content.issuperset(feature):
                location = found
                break

    print("Rez bin dir found: %s" % location)

    env.PYTHONHOME = ""
    env.PYTHONPATH = ""
    env.PATH.prepend(location)
