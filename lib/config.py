import os
import json

WORKING_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(WORKING_PATH, "config.json")

# Default config.
CONFIG = {
    "dynamic_modules": {
        "bash": {
            "enabled": False
        },
        "css": {
            "enabled": False
        },
        "html": {
            "enabled": False
        },
        "javascript": {
            "enabled": False
        },
        "python": {
            "enabled": False
        }
    }
}


def save_config():
    global CONFIG
    global CONFIG_PATH
    try:
        configData = json.dumps(CONFIG, sort_keys=True, indent=4,
            ensure_ascii=False)
        with open(CONFIG_PATH, "w+") as f:
            f.write(configData)  # Save config to file.
    except Exception as e:
        print("Could not save config file: %s" % str(e))


def load_config():
    global CONFIG
    global CONFIG_PATH
    try:
        if os.path.isfile(CONFIG_PATH):  # If the config file exists.
            with open(CONFIG_PATH, "r") as f:
                CONFIG = json.loads(f.read())  # Load saved configuration.
        else:  # If the config file does not exist.
            save_config()  # Save the default config to file.
    except Exception as e:
        print("Could not load config file: %s" % str(e))


def get_config():
    global CONFIG
    return CONFIG


load_config()
