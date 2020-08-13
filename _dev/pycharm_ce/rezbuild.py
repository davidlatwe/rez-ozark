
import os
import sys
import shutil


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

    bin_src = os.path.join(source_path, "bin")
    bin_dst = os.path.join(dst, "bin")
    shutil.copytree(bin_src, bin_dst)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
