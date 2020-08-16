
import os
ModifyList = globals()["ModifyList"]

packages_path = ModifyList(append=[
    # (TODO) Might need to put this in somewhere else, so the profile
    #   package won't mixed up with regular packages.
    os.getenv("OZARK_LOCATION_INSTALL", "mongozark@install.rez.ozark"),
    os.getenv("OZARK_LOCATION_RELEASE", "mongozark@release.rez.ozark"),
])

debug_plugins = False  # Turn this on if plugin not loaded.

plugin_path = ModifyList(append=[
    os.path.dirname(os.path.dirname(__file__))
])


__release_uri = os.getenv("OZARK_MONGODB_RELEASE", "localhost:27017")
__install_uri = os.getenv("OZARK_MONGODB_INSTALL",
                          "montydb://" + os.path.expanduser("~/ozark-data"))

plugins = {
    "package_repository": {
        "mongozark": {
            "uri": {
                "install": __install_uri,
                "release": __release_uri,
            },
        },
    }
}
