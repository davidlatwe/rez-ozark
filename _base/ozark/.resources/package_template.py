
name = "{profile_name}"

version = "0.1.0"

authors = [
    # profile owners
]

features = [
    # List out features of this profile,
    # e.g. "show.ongoing", "dev.pipeline", ...
]

positions = [
    # List out which role can have access to this profile,
    # e.g. "artist", "technical", "developer", "admin", ...
]

requires = [
    # List out profile required packages,
    # e.g. "maya-2020", "python-3", "pycharm", ...
]


# Set up environment
def commands():
    env = globals()["env"]


"""
!!! Do not change following attributes !!!
"""
build_command = False
no_variants = True
