
name = "rezcore"

description = "Find and enter Rez's virtual env, use with caution."

version = "1.0.0"

build_command = False


def commands():
    import os
    from rez.system import system
    env = globals()["env"]

    location = system.rez_bin_path

    if location is None:
        raise Exception("Rez bin dir not found.")

    venv_path = os.path.dirname(location)

    env.PYTHONHOME.unset()
    env.PYTHONPATH = ""
    env.PATH.prepend(venv_path)
    env.REZ_CORE_BIN_PATH = location
