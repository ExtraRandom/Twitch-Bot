import cfg
# import utils
import aiohttp


def youtube():
    return "YouTube Channel: {}".format(cfg.TUBE)


def twitter():
    return "Twitter: {}".format(cfg.TWIT)

async def ow():
    user = cfg.OW_USER.replace("#", "-")  # Just in case config has a # instead of a -
    link = "https://owapi.net/api/v3/u/{}/stats?format=json_pretty".format(user)
    headers = {
        'User-Agent': "SmellyFeetBot"
    }

    try:
        with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(link)as resp:
                data = await resp.json()

                stats = data[cfg.OW_REGION.lower()]['stats']['quickplay']

                level = stats['overall_stats']['level']
                elims = str(stats['average_stats']['eliminations_avg']).replace(".0", "")
                death = str(stats['average_stats']['deaths_avg']).replace(".0", "")
                ptime = str(stats['game_stats']['time_played']).replace(".0", "")
                medal = str(stats['game_stats']['medals']).replace(".0", "")

                return "In Overwatch I am currently level {}, with {} hours played (QuickPlay). My average " \
                       "Elims/Deaths is {}/{}. I have earned {} medals.".format(level, ptime, elims, death, medal)

    except Exception as e:
        print("Error in Overwatch Command: {}".format(e))
        return "Error getting Overwatch Stats"





