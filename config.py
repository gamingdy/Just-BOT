import json


with open("config.json") as conf:
    config_file = json.load(conf)
    TOKEN = config_file["TOKEN"]
