# utils.py
# A bunch of utility functions

import cfg
import json
import requests

import time, _thread as thread
from time import sleep

# Function: chat
# Send a chat message to the server.
#    Parameters:
#      sock -- the socket over which to send the message
#      msg  -- the message to send


def chat(sock, msg):
    channel = cfg.CHAN.replace("#", "")  # A weird fix that I'm not happy with but it makes the bot work again so It'll
    # do for no, TODO fix this if it ever breaks something
    sock.send(("PRIVMSG #{} :{}\r\n".format(channel, msg)).encode('utf-8'))

# Function: ban
# Ban a user from the channel
#   Parameters:
#       sock -- the socket over which to send the ban command
#       user -- the user to be banned


def ban(sock, user):
    chat(sock, ".ban {}".format(user))

# Function: timeout
# Timeout a user for a set period of time
#   Parameters:
#       sock -- the socket over which to send the timeout command
#       user -- the user to be timed out
#       seconds -- the length of the timeout in seconds (default 600)


def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds))

# Function: threadFillOpList
# In a separate thread, fill up the op list


def threadFillOpList():
    # TODO make sure this isn't broken

    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/{}/chatters".format(cfg.CHAN)
            resp = requests.get(url)

            if resp.status_code == requests.codes.ok:
                cfg.oplist.clear()
                data = json.loads(resp.text)
                # print("chatters {}".format(data["chatter_count"]))

                for p in data["chatters"]["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    cfg.oplist[p] = "staff"

        except Exception as e:
            print("Failed to update Op List: {}".format(e))
        # print("Updated Op List")
        sleep(60)


def isOp(user):
    return user in cfg.oplist