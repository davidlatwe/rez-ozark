
name = "Qt.py"

uuid = "repository.Qt.py"

version = ""

description = "Minimal Python 2 & 3 shim around all Qt bindings - "\
              "PySide, PySide2, PyQt4 and PyQt5."

authors = []

variants = [
    ["PyQt5"],
    ["PySide2"],
    ["PyQt4"],
    ["PySide"],
]


build_command = "python {root}/rezbuild.py {install}"


def commands():
    env.PYTHONPATH.prepend("{root}/payload")
