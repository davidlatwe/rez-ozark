
import os
import shutil
import subprocess
from rez.config import config as config_


def init():
    ozark_root = os.environ["REZ_OZARK_ROOT"]
    template = os.path.join(ozark_root, ".resources", "package_template.py")
    dst = os.path.join(os.getcwd(), "package.py")
    if os.path.exists(dst):
        print("package.py already exists in current directory.")
        return

    shutil.copy(template, dst)


def ls(location=None):
    if location:
        location = get_location(location)
        if location is None:
            raise Exception("Location '%s' not registered in mongozark.")

        args = [
            "rez-search",
            "--paths",
            location,
        ]

    else:
        locations = get_location()
        if not locations:
            raise Exception("Not any location registered in mongozark.")

        args = [
            "rez-search",
            "--paths",
            os.path.pathsep.join(locations)
        ]

    subprocess.call(args)


def build(location=None):
    if location:
        location = get_location(location)
        if location is None:
            raise Exception("Location '%s' not registered in mongozark.")

        args = [
            "rez-build",
            "--install",
            "--prefix",
            location,
        ]

    else:
        args = [
            "rez-build",
        ]

    subprocess.check_call(args)


def get_location(name=None):
    config = get_config()
    if name:
        return getattr(config.location, name, None)
    else:
        return list(config.location.values())


def get_config():
    return config_.plugins.package_repository.mongozark
