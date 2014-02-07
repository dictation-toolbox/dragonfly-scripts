"""Configuration module, saves the config in a json file.

Keeping the configuration in a json file has the advantage that it can be
changed in runtime by voice commands.
For instace, the dynamic grammars saves their state of enabled or disabled in
runtime. If Natlink is reloaded or Dragon is restarted, the previous state is
loaded and the previously enabled dynamic grammars are enabled again.

The advantage of using a flat structure in the config, as opposed to a nested,
is that the code for reading and writing becomes very simple.

Example config:
{
    "aenea.enabled": false,
    "aenea.path": null,  // Set path if Aenea is outside MacroSystem dir.
    "dynamics.bash.enabled": true,
    "dynamics.css.enabled": false,
    "dynamics.git.enabled": false,
    "dynamics.html.enabled": false,
    "dynamics.javascript.enabled": false,
    "dynamics.python.enabled": false,
    "system.base_path": "C:\\Natlink\\Natlink\\MacroSystem"
}
"""
import os
import json

WORKING_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(WORKING_PATH, "config.json")
CONFIG = {}


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
