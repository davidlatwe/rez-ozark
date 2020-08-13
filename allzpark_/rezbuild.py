
import os
import sys
import shutil
import subprocess


def build(source_path, build_path, install_path, targets=None):
    targets = targets or []

    if "install" in targets:
        dst = install_path
    else:
        dst = build_path

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    args = ["python", "setup.py", "--quiet", "build", "--build-base", dst]
    subprocess.check_call(args, cwd=source_path)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
