
import sys
import argparse


def main(argv=None):
    argv = argv or sys.argv

    parser = argparse.ArgumentParser(description="Ozark profile producer")
    parser.add_argument("location", nargs="?", const=True, default=False,
                        help="")

    opt = parser.parse_args(argv)

    """
    rez-build --install --prefix mongozark@install.rez.ozark
    rez-build --install --prefix mongozark@release.rez.ozark
    """
