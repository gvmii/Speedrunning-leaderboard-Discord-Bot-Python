# Speedrunning-leaderboard-Discord-Bot-Python © 2022 by Iwakura Megumi is
# licensed under CC BY-NC 4.0. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/


import json
import os
import sys
from datetime import datetime, timedelta

import sqlite3
import aiofiles
import aiohttp
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from rich import print, console

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    status=nextcord.Status.do_not_disturb,
    activity=nextcord.Game(name="https://github.com/gvmii"),
    intents=intents,
)
console = console.Console()
load_dotenv()


async def read_config():
    #tries to open config.json, if it fails it will return false and prompt the user to run setup.py
    try:
        async with aiofiles.open(
            "data/config.json", mode="r", encoding="utf8"
        ) as jsonfile:
            contents = await jsonfile.read()
    except FileNotFoundError:
        print(f'[red]config file not found. try running setup.py[/red]')
        return False

    config = json.loads(contents)
    console.log("Config loaded [green]successfully[/green].")
    print(config)
    return config


# On ready, do this.
@bot.event
async def on_ready():
    config = await read_config()
    #if config is not False do stuff, otherwise quit & tell user to run setup.py
    if config:
        if not config["channel_id"]:
            config = await read_config()
        try:
            channel_id = int(config["channel_id"])
            console.log(f"Channel ID Set to: {channel_id}.")
        except Exception as e:
            console.log(f"[red]Error[/red]: Couldn't read channel id: {e}")
            sys.exit(1)

        print(f"Logged in as {bot.user}.")
        channel = bot.get_channel(channel_id)
        console.log(
            f"Channel #{channel.name} ({channel.id}) [green]found[/green]."
        )
    else:
        exit()


@bot.event
async def on_command_error(ctx, error):
    console.log(f"[red]Error[/red]: {str(error)}")


@bot.slash_command()
async def ping(ctx):
    await ctx.send("pong")


async def write_to_file(data, file):
    async with aiofiles.open(file, "w") as f:
        await f.write(json.dumps(data))
        print("Done writing JSON data into .json file")


async def read_dict(file):
    async with aiofiles.open(file, "r") as f:
        loaded_dict = json.loads(await f.read())
        with_int_keys = {int(key): value for key, value in loaded_dict.items()}
    return with_int_keys


async def read_list(file):
    async with aiofiles.open(file, "r") as f:
        loaded_list = json.loads(await f.read())
    return loaded_list


async def deltify_time(time):
    # This might be slow because try excepts are slow in Python, but whatever.
    # TODO: Make this a bit more efficient
    try:
        t = datetime.strptime(time, "%H:%M:%S.%f").time()
        delta = timedelta(
            hours=t.hour,
            minutes=t.minute,
            seconds=t.second,
            microseconds=t.microsecond,
        )
    except ValueError:
        return ValueError
    return delta


VALID_CATEGORIES = ["ANY%", "ARB", "SL"]


async def validate_category(category):
    global VALID_CATEGORIES
    c = category.upper()
    if c in VALID_CATEGORIES:
        return True
    else:
        return False

#command to change the channel id. not too neccessary and will probably remove later
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def setchannelid(ctx, channel_id):
    async with aiofiles.open("config.json", mode="r", encoding="utf8") as f:
        contents = await f.read()
        thing = json.loads(contents)

    thing["channel_id"] = channel_id

    await write_to_file(thing, "config.json")

    embed = nextcord.Embed(title="Success",description=f"Successfully changed the Channel ID to '{channel_id}'",color=nextcord.Color.blurple())
    await ctx.send(embed=embed)

@bot.slash_command()
async def register(ctx):
    user_id = ctx.author.id
    loaded_file = await read_dict("times.json")
    writing_template = {
        user_id: {
            "any%": {"time": "", "state": ""},
            "arb": {"time": "", "state": ""},
        }
    }
    loaded_file.update(writing_template)
    await write_to_file(loaded_file, "times.json")


@bot.slash_command()
async def favorite_song(ctx, song):
    loaded_users = await read_list("user_songs.json")
    user_id = ctx.author.id
    song_to_write = {user_id: song}
    loaded_users.update(song_to_write)
    print(loaded_users)
    await write_to_file(loaded_users, "user_songs.json")


@bot.slash_command()
async def submit_time(ctx, category: str, time: str):
    user_id = ctx.author.id
    loaded_file = await read_dict("times.json")
    if await validate_category(category) is False:
        global VALID_CATEGORIES
        await ctx.send(
            "Please write a valid category. Valid categories are "
            + str(VALID_CATEGORIES)
        )
        return
    # TODO: Fix this jank thing
    delta = await deltify_time(time)
    try:
        formatted_time = str(delta.total_seconds())
    except AttributeError:
        await ctx.send(
            "Please write your time in the following format: H:M:S.ms"
        )
        return

    else:
        if user_id in loaded_file:
            loaded_file[user_id][category]["time"] = formatted_time
            loaded_file[user_id][category]["state"] = "NEW"

            await write_to_file(loaded_file, "times.json")
            await ctx.send(
                f"Successfully submitted time of **{str(delta)}** for the "
                f"category **{category}** For the user {ctx.author} with ID "
                f"{user_id} at {datetime.now()}"
            )
        else:
            await ctx.send("registrate")
            return


@bot.slash_command()
async def personal_best(
        ctx, category: str = "Any%", user: nextcord.Member = None
):
    user_id = ctx.author.id
    loaded_file = await read_dict("times.json")

    user = user or ctx.author

    if user.id in loaded_file:
        pb = float(loaded_file[user_id].get(category))
        await ctx.send(
            f"{user.mention}'s {category} time is {str(timedelta(seconds=pb))}"
        )


@bot.slash_command()
async def leaderboard(ctx, category):
    loaded_file = await read_dict("times.json")
    dict_to_sort = {}

    for user_id, time in loaded_file.items():
        print(time[category])
        dict_to_sort.update({user_id: float(time[category]["time"])})

    sorted_obj = dict(sorted(dict_to_sort.items(), key=lambda i: i[1]))

    embed = nextcord.Embed(title="Leaderboard")
    print(sorted_obj.items())
    number = 1
    for userid, time in sorted_obj.items():
        user = await bot.fetch_user(int(userid))
        embed.add_field(
            name=f"{number} - {user.name}",
            value=str(timedelta(seconds=time)).replace("0000", ""),
            inline=False,
        )
        number += 1

    await ctx.send(embed=embed)

# Phew, this is harder than I initially expected...
# @bot.command()
# async def best_times(ctx):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(
#             "https://www.speedrun.com/api/v1/runs",
#             params={"game": "Celeste", "category": "any%"},
#         ) as r:
#             print(await r.json())
#             for i in r.json:
#                 print(i)


bot.run(os.getenv("TOKEN"))
