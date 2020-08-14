
import os
ModifyList = globals()["ModifyList"]


packages_path = ModifyList(append=[
    "mongozark@rez.ozark"  # <repo>@<dbName>.<colName>
])

plugin_path = ModifyList(append=[
    "{root}/rezplugins"
])

plugins = {
    "package_repository": {
        "mongozark": {
            "uri": os.getenv("OZARK_MONGODB", "localhost:20717")
        },
    }
}
