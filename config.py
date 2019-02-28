import json

def loadConfig(filename="./.config/dev.config.json"):
    print("Begin load config file: {0}".format(filename))
    with open(filename) as fh:
        config = json.load(fh)
        print("Load configuration successfully!")
        return config
