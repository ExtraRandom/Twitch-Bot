# cfg.py
# Contains the configurations for the bot

HOST = "irc.chat.twitch.tv"  # "irc.twitch.tv"
PORT = 6667  # 6667
NICK = ""  # Username
PASS = "oauth:"  # Chat Token
CHAN = ""
RATE = (20/30)

oplist = {}

# COMMAND CONFIGS
TUBE = ""  # Link to channel
TUBE_ACTIVE = True  # If false the command can not be used
TUBE_ALIAS = {"!yt", "!youtube"}  # All aliases for the command

TWIT = ""  # Link to twitter page
TWIT_ACTIVE = True
TWIT_ALIAS = {"!twit", "!twitter", "!tweet", "!tweeter", "!tw"}

OW_ACTIVE = False
OW_USER = ""  # Put your BattleTag here, Replace the # with -
OW_REGION = "EU"  # KR (Korea/Asia) and US (USA/Australia) are the other options
OW_ALIAS = {"!ow", "!overwatch"}

DISCORD = ""
DISCORD_ACTIVE = False
DISCORD_ALIAS = {"!discord", "!ts", "!teamspeak", "!voice", "!join", "!discordserver", "!server"}

UPTIME_ACTIVE = False
UPTIME_ALIAS = False

HELP = ""
HELP_ACTIVE = True
HELP_ALIAS = {"!help", "!commands", "!cmdlist", "!list", "!commandlist", "!botcommands"}

DONATE = {"Patreon - [Patreon Link]", "Other - [Other Link]"}  # Example of how I would format it
DONATE_ACTIVE = False
DONATE_ALIAS = {"!donate", "!support"}

FB = "Link Goes Here"
FB_ACTIVE = False
FB_ALIAS = {"!fb", "!face", "!facebook"}