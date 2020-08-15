
import os
ModifyList = globals()["ModifyList"]

packages_path = ModifyList(append=[
    # (TODO) Might need to put this in somewhere else, so the profile
    #   package won't mixed up with regular packages.
    os.getenv("OZARK_LOCATION", "mongozark@rez.ozark"),
])

debug_plugins = False  # Turn this on if plugin not loaded.

plugin_path = ModifyList(append=[
    os.path.dirname(os.path.dirname(__file__))
])

plugins = {
    "package_repository": {
        "mongozark": {
            "uri": os.getenv("OZARK_MONGODB", "localhost:27017"),
            "montydb": {
                "engine": "flatfile",
            }
        },
    }
}
