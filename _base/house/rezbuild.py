
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

    env_src = os.path.join(source_path, ".env")
    env_dst = os.path.join(dst, ".env")
    if os.path.isfile(env_src):
        shutil.copy(env_src, env_dst)
    else:
        print(".env file not exists. No env will be set.")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
