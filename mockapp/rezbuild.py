
import os
import sys
import stat
import shutil
import platform


bash = """
#!/usr/bin/env bash
python -u -m mockapp {tool}
"""

cmd = """
@echo off
call python -u -m mockapp {tool}
"""


def build(source_path, build_path, install_path, targets=None):
    targets = targets or []

    if "install" in targets:
        targets.remove("install")
        dst = install_path
    else:
        dst = build_path

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    dir_src = os.path.join(source_path, "python")
    dir_dst = os.path.join(dst, "python")
    shutil.copytree(dir_src, dir_dst)

    tools = targets

    if platform.system() == "Windows":
        script = cmd
        ext = ".bat"
    else:
        script = bash
        ext = ""

    bin_dir = os.path.join(dst, "bin")
    os.makedirs(bin_dir)
    for tool in tools:
        bin_path = os.path.join(bin_dir, tool) + ext
        with open(bin_path, "w") as bin_:
            bin_.write(script.format(tool=tool))

        # chmod +x
        st = os.stat(bin_path)
        os.chmod(bin_path, st.st_mode | stat.S_IEXEC)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
