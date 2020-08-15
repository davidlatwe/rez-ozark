
import os
import sys
import shutil
import platform
import subprocess


additional_rez_core_dependencies = [
    "montydb",
    "pymongo",
]


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

    print("Installing additional dependencies into Rez core")
    install_rez_dependency(additional_rez_core_dependencies)

    for dirname in ["bin", "config", "python", "rezplugins"]:
        dir_src = os.path.join(source_path, dirname)
        dir_dst = os.path.join(dst, dirname)
        shutil.copytree(dir_src, dir_dst)

    print("Ozark installed.")


def install_rez_dependency(modules):
    bin_dir = find_rez_bin_dir()
    if bin_dir is None:
        raise Exception("Rez installation not found. Is rez bin in $PATH ?")

    args = [
        "rez-env",  # jump to clean env so we can touch rez core
        "--",
        "pip",
        "install"
    ] + modules

    subprocess.check_call(args, cwd=bin_dir)


def find_rez_bin_dir():
    if platform.system() == "Windows":
        finder = "where"
    else:
        finder = "which"

    try:
        locations = subprocess.check_output([finder, "rez"],
                                            universal_newlines=True)
    except subprocess.CalledProcessError:
        return

    rez_exec = locations.split("\n")[0]
    bin_dir = os.path.dirname(os.path.dirname(rez_exec))

    return bin_dir


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
