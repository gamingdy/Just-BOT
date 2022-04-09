import json


with open("config.json") as conf:
    config_file = json.load(conf)
    print(config_file)
    TOKEN = config_file["TOKEN"]
