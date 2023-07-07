import json
import sqlite3
import sys

with open("config.json") as conf:
    config_file = json.load(conf)
    TOKEN = config_file["TOKEN"]
    database = sqlite3.connect(config_file["database"])
    debug_guild = config_file["debug"][1] if config_file["debug"][0] else None
    debug_channel = config_file["debug_channel"]

if not isinstance(debug_channel, int) or debug_channel == 0:
    print("Debug channel must be a valid guild id")
    sys.exit()

with open("data/extension.json", "w") as ext_list:
    json.dump({}, ext_list, indent=4)

ELEMENTS_PER_PAGE = 5
