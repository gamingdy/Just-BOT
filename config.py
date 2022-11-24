import json
import sqlite3

with open("config.json") as conf:
    config_file = json.load(conf)
    TOKEN = config_file["TOKEN"]
    database = sqlite3.connect(config_file["database"])
    debug_guild = config_file["debug"][1] if config_file["debug"][0] else None

with open("data/extension.json", "w") as ext_list:
    json.dump({}, ext_list, indent=4)
