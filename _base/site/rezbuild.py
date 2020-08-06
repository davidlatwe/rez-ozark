
import os
import sys
import shutil


def logger():
    import logging

    package_name = os.environ["REZ_BUILD_PROJECT_NAME"]
    log_name = package_name + ".build"

    # (TODO) Add formatter

    log_handler = logging.StreamHandler()
    log = logging.getLogger(log_name)
    log.addHandler(log_handler)
    log.setLevel(logging.INFO)

    return log


def build(source_path, build_path, install_path, targets=None):
    log = logger()
    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    scr = os.path.join(source_path, "src")
    shutil.copytree(scr, dst)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
