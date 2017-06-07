import json


file = "config.json"
default_settings = {
    "HOST": "irc.chat.twitch.tv",
    "PORT": "6667",
    "NICK": None,
    "PASS": None,
    "CHAN": None,
    "RATE": 1.5
}
# TODO finish writing how to setup in /docs/setup.md and then link to it in readme


def read_settings():
    try:
        with open(file) as data_file:
            data = json.load(data_file)
        return data
    except FileNotFoundError:
        return None


def create_file():
    with open(file, 'w') as data_file:
        json.dump(default_settings, data_file)

config = read_settings()
if config is None:
    print("No Config File, Creating one now")
    create_file()
    config = read_settings()



"""


try:
    with open(file) as data_file:
        data = json.load(data_file)
    print(data)
except FileNotFoundError:
    print("oh no")
    with open(file, 'w') as data_file:
        json.dump(default_settings, data_file)

"""

