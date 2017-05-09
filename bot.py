import cfg
import utils  # import sql
import socket
import re
import time, _thread as thread
from time import sleep
from datetime import datetime

import commands

import asyncio


class Command(object):
    cmd = ""
    response = ""
    description = ""
    op = 0

    def __init__(self, cmd, response, description, op):
        self.cmd = cmd
        self.response = response
        self.description = description
        self.op = op


async def main():

    print("Bot Started at: {} UTC".format(datetime.utcnow()))

    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Bot Online")

    thread.start_new_thread(utils.threadFillOpList, ())

    while True:
        response = s.recv(1024).decode("utf-8")
        # print(response)

        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))  # print("Pong!")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

            # print(message)
            cmd = message.strip().split(" ")

            if cmd[0] != ":tmi.twitch.tv" and cmd[0] != ":{0}!{0}@{0}.tmi.twitch.tv".format(cfg.CHAN):
                print("cmd: {}".format(cmd[0]))
                if len(cmd) > 1:
                    print("args: {}".format(cmd[1:]))

            if cmd[0] == "!test":
                utils.chat(s, "Hello there, {}".format(username))
                print("ye1")

            if cmd[0] in cfg.TUBE_ALIAS:  # cmd[0] == "!yt" or cmd[0] == "!youtube":
                if cfg.TUBE_ACTIVE:
                    utils.chat(s, commands.youtube())

            if cmd[0] in cfg.TWIT_ALIAS:
                if cfg.TWIT_ACTIVE:
                    utils.chat(s, commands.twitter())

            if cmd[0] in cfg.OW_ALIAS:
                if cfg.OW_ACTIVE:
                    utils.chat(s, await commands.ow())

        sleep(1)

    # utils.chat(s, "Bot Shutting Down");
if __name__ == "__main__":
    # main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
