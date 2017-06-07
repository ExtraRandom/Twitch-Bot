import cfg
import utils
import socket
import re
import time
import _thread as thread
from time import sleep
from datetime import datetime
import commands
import asyncio  # import json

import config


def config_checks():
    """If all configs are fine returns true, if not returns false"""
    config_data = config.read_settings()
    msg = ""
    if config_data["NICK"] is None:
        msg += "'NICK' not set. "
    if config_data["PASS"] is None:
        if msg != "":
            msg += "\n"
        msg += "'PASS' not set"

    return True, config_data

async def main():

    ready, data = config_checks()
    if not ready:
        return
    else:
        NICK = data["NICK"]
        PASS = data["PASS"]
        CHAN = data["CHAN"]

        if NICK is None:
            print("Error: No value for NICK. Check config.json. Stopping bot.")
            return
        if CHAN is None:
            print("Error: No value for CHAN. Check config.json. Stopping bot.")
            return

    print("Bot Started at: {} UTC".format(datetime.utcnow()))

    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    # s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    # s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    # s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))
    # TODO make sure the # doesn't cause essues else where

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Bot Online")

    thread.start_new_thread(utils.threadFillOpList, ())

    cooling = {}

    def cooldown(command, downtime=10):
        if command not in cooling or time.time() - cooling[command] > downtime:
            cooling[command] = time.time()
            return 0

        else:
            not_cd_time = cooling[command] - time.time()
            cd_time = str(not_cd_time).split(".")[0].replace("-", "")
            actual_cooldown = downtime - int(cd_time)
            utils.chat(s, "Command '{}' is on cooldown for {} more seconds!".format(command, actual_cooldown))
            return 1

    while True:
        response = s.recv(1024).decode("utf-8")  # print(response)

        print(response)
        # utils.chat(s, "ech")

        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

            # print(message)

            cmd = message.strip().split(" ")

            if cmd[0] != ":tmi.twitch.tv" and cmd[0] != ":{0}!{0}@{0}.tmi.twitch.tv".format(cfg.NICK.lower()) \
                    and str(cmd[0]).startswith("!"):
                print("User '{}' Called Command: {}".format(username, cmd[0]))
                if len(cmd) > 1:
                    print("Args Given: {}".format(cmd[1:]))
                """
                else:
                    log = True
                    if log:
                        print("User '{}' sent message: {}".format(username, message))
                """
            else:
                if cmd[1] == "NOTICE":
                    if cmd[2] == "*":
                        if cmd[3] == ":Improperly":
                            print("Error: OAUTH / PASS is wrong. Check config.json. Stopping Bot.")
                            return
                # print(cmd)

            # TODO admin commands (ban, timeout)

            if cmd[0] == "!wew":
                utils.chat(s, "wew!")

            if cmd[0] == "!ping":
                if cooldown("ping", 60) == 0:
                    utils.chat(s, "Pong!")

            if cmd[0] in cfg.TUBE_ALIAS:
                if cfg.TUBE_ACTIVE:
                    if cooldown("youtube") == 0:
                        utils.chat(s, commands.youtube())

            if cmd[0] in cfg.TWIT_ALIAS:
                if cfg.TWIT_ACTIVE:
                    if cooldown("twitter") == 0:
                        utils.chat(s, commands.twitter())

            if cmd[0] in cfg.OW_ALIAS:
                if cfg.OW_ACTIVE:
                    if cooldown("ow") == 0:
                        utils.chat(s, await commands.ow())

            if cmd[0] in cfg.FB_ALIAS:
                if cfg.FB_ACTIVE:
                    if cooldown("facebook") == 0:
                        utils.chat(s, commands.facebook())

            if cmd[0] in cfg.DONATE_ALIAS:
                if cfg.DONATE_ACTIVE:
                    if cooldown("donate") == 0:
                        utils.chat(s, commands.donate())

            if cmd[0] in cfg.HELP_ALIAS:
                if cfg.HELP_ACTIVE:
                    if cooldown("help", 5) == 0:
                        utils.chat(s, commands.give_help())

            if cmd[0] == "!ops":
                if cooldown("ops", 60) == 0:
                    utils.chat(s, cfg.oplist)

            """
            if cmd[0] == "!updateops":
                if utils.isOp(username):
                    utils.threadFillOpList()
            """

        sleep(1 / cfg.RATE)

    # utils.chat(s, "Bot Shutting Down");
if __name__ == "__main__":
    # main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
