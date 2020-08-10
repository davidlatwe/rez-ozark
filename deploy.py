
import os
import sys
import shutil
import functools
import subprocess
import _packages


def confirm(msg):
    try:
        _input = raw_input
    except NameError:
        _input = input

    try:
        reply = _input(msg).lower().rstrip()
        return reply in ("", "y", "yes", "ok")
    except EOFError:
        return True  # On just hitting enter
    except KeyboardInterrupt:
        return False


def deploy_package(packages=None, release=False):
    for pkg in _packages.packages:
        if packages and pkg["name"] not in packages:
            continue

        _packages.deploy(pkg, release)


def install_rez(location=None):
    location = functools.reduce(lambda path, f: f(path),
                                [location or "~/rez/core",
                                 os.path.expanduser,
                                 os.path.expandvars,
                                 os.path.normpath])

    print("Rez will be installed to %s" % location)
    print("Directory will be removed if exists.")
    if not confirm("Do you want to continue ? [Y/n]\n"):
        print("Cancelled")
        return

    if os.path.isdir(location):
        shutil.rmtree(location)
    os.makedirs(location)

    args = [sys.executable, "install.py", "-v", location]
    assert subprocess.check_call(args, cwd="./rezsrc") == 0

    return location


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="?")
    parser.add_argument("--install-rez", action="store_true")
    parser.add_argument("--with-config", action="store_true")
    parser.add_argument("--with-package", action="store_true")
    parser.add_argument("packages", nargs="*")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--yes", action="store_true")

    opt = parser.parse_args()

    if opt.install_rez:
        dst = install_rez(opt.location)

        # Update environment for later subprocess deploy
        os.environ["PATH"] = os.path.pathsep.join([dst, os.environ["PATH"]])

    config_path = None
    if opt.with_config:
        config_path = os.path.join(os.path.dirname(__file__), "rezconfig.py")

    if opt.with_package:
        if opt.install_rez:
            if not confirm("Continue to deploy packages ? [Y/n]\n"):
                print("Cancelled")
                sys.exit(0)

        if config_path:
            print("Deploying packages with this config: %s" % config_path)
            if not opt.yes:
                if not confirm("Are you sure ? [Y/n]\n"):
                    print("Cancelled")
                    sys.exit(0)

            os.environ["REZ_CONFIG_FILE"] = config_path

        deploy_package(opt.packages, opt.release)

        print("=" * 30)
        print("All deployed.")

        if config_path:
            print("Packages were deployed with config: %s" % config_path)
            print("Remember to add it into $REZ_CONFIG_FILE")
