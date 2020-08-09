
import _deploy


def deploy(release=None):
    for pkg in _deploy.packages:
        if opt.package and opt.package != pkg["name"]:
            continue

        _deploy.deploy(pkg, release)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--package")
    parser.add_argument("--release", action="store_true")

    opt = parser.parse_args()

    if opt.deploy:
        deploy(opt.release)
