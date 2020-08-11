
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
    parser.add_argument("--install-rez", nargs="?", const=True, default=False,
                        help="Rez install path if you want to install it. "
                             "If enabled but no path given, Rez will be "
                             "installed in ~/rez/core")
    parser.add_argument("--deploy-package", action="store_true",
                        help="Deploy packages from this repository.")
    parser.add_argument("--with-config", nargs="?", const=True, default=False,
                        help="Deploy packages with config ($REZ_CONFIG_FILE). "
                             "If enabled but no config path(s) given, "
                             "./rezconfig.py will be used.")
    parser.add_argument("packages", nargs="*",
                        help="Deploy only these packages. Deploy ALL if no "
                             "specification.")
    parser.add_argument("--release", action="store_true",
                        help="Deploy to package releasing location.")
    parser.add_argument("--yes", action="store_true",
                        help="Yes to all.")

    opt = parser.parse_args()

    if opt.install_rez:
        use_default = opt.install_rez is True
        dst = install_rez(location=None if use_default else opt.install_rez)

        # Update environment for later subprocess deploy
        os.environ["PATH"] = os.path.pathsep.join([dst, os.environ["PATH"]])

    config_path = None
    if opt.with_config:
        use_default = opt.with_config is True
        if use_default:
            config_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "rezconfig.py"))
        else:
            config_path = opt.with_config

    if opt.deploy_package:
        if opt.install_rez:
            if not confirm("Continue to deploy packages ? [Y/n]\n"):
                print("Cancelled")
                sys.exit(0)

        if config_path:
            print("Deploying packages with $REZ_CONFIG_FILE=%s" % config_path)
            if not opt.yes:
                if not confirm("Are you sure ? [Y/n]\n"):
                    print("Cancelled")
                    sys.exit(0)

            os.environ["REZ_CONFIG_FILE"] = config_path

        deploy_package(opt.packages, opt.release)

        print("=" * 30)
        print("SUCCESS!\n")

        if config_path:
            print("Deployed with $REZ_CONFIG_FILE=%s" % config_path)
            print("Use the same $REZ_CONFIG_FILE when accessing packages.\n")
