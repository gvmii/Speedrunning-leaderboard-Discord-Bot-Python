# Speedrunning-leaderboard-Discord-Bot-Python © 2022 by Iwakura Megumi is
# licensed under CC BY-NC 4.0. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/


import json
import os
import sys
from datetime import datetime, timedelta
import aiofiles
import nextcord
import sqlite3
import srcomapi, srcomapi.datatypes as dt
from dotenv import load_dotenv
from nextcord.ext import commands
from rich import print, console

intents = nextcord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    status=nextcord.Status.do_not_disturb,
    activity=nextcord.Game(name="https://github.com/gvmii"),
    intents=intents,
)
console = console.Console()
load_dotenv()

# Inititialize connection to the SQLITE3 database

con = sqlite3.connect("data/database.db")
cur = con.cursor()

async def read_config():
    # tries to open config.json, if it fails it will return false and prompt
    # the user to run setup.py
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
    # if config is not False do stuff, otherwise quit & tell user to run
    # setup.py
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


# @bot.event
# async def on_command_error(ctx, error):
#    console.log(f"[red]Error[/red]: {str(error)}")


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


VALID_CATEGORIES = ["ANY%", "ARB", "TRUEENDING"]


async def validate_category(category):
    global VALID_CATEGORIES
    c = category.upper()
    if c in VALID_CATEGORIES:

        return True
    else:
        return False


# command to change the channel id. not too neccessary and will probably
# remove later
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def setchannelid(ctx, channel_id):
    async with aiofiles.open("config.json", mode="r", encoding="utf8") as f:
        contents = await f.read()
        thing = json.loads(contents)

    thing["channel_id"] = channel_id

    await write_to_file(thing, "config.json")

    embed = nextcord.Embed(title="Success", description=f"Successfully changed the Channel ID to '{channel_id}'",
                           color=nextcord.Color.from_rgb(255, 38, 96))
    await ctx.send(embed=embed)


@bot.slash_command()
async def register(ctx):
    user_id = ctx.user.id
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
async def submit_time(ctx, category: str, time: str):
    user_id = ctx.user.id
    if await validate_category(category) is False:
        global VALID_CATEGORIES
        await ctx.send(
            "Please write a valid category. Valid categories are "
            + str(VALID_CATEGORIES)
        )
        return
    if category == 'any%':
        category = 'anypercent'
    # TODO: Fix this jank thing
    delta = await deltify_time(time)
    try:
        formatted_time = str(delta.total_seconds())
    except AttributeError:
        await ctx.send(
            "Please write your time in the following format: H:M:S.ms"
        )
        return

    cur.execute(f"""
    INSERT OR REPLACE INTO {category} VALUES
        ({user_id}, {formatted_time})
    """)
    con.commit()

    await ctx.send(
        f"Successfully submitted time of **{str(delta)}** for the "
        f"category **{category}** For the user {ctx.user} with ID "
        f"{user_id} at {datetime.now()}"
    )


@bot.slash_command()
async def personal_best(
        ctx, category: str = "Any%", user: nextcord.Member = None
):
    user = user or ctx.user

    cur.execute(f"""
    SELECT MIN(TIME) FROM {category} WHERE USER_ID = {user.id}

    """)
    time = cur.fetchall()[0][0]

    await ctx.send(f"{user.mention}'s {category} time is {str(timedelta(seconds=time)).replace('0000', '') }")


@bot.slash_command()
async def leaderboard(ctx, category):

        ## SAVING THIS ABSOLUTE FUCKING MONSTROSITY FOR PROSPERITY ##

        # loaded_file = await read_dict("times.json")
        # dict_to_sort = {}

        # for user_id, time in loaded_file.items():
        #     print(time[category])
        #     dict_to_sort.update({user_id: float(time[category]["time"])})

        # sorted_obj = dict(sorted(dict_to_sort.items(), key=lambda i: i[1]))

        # embed = nextcord.Embed(title="Leaderboard")
        # print(sorted_obj.items())
        # number = 1
        # for userid, time in sorted_obj.items():
        #     user = await bot.fetch_user(int(userid))
        #     embed.add_field(
        #         name=f"{number} - {user.name}",
        #         value=str(timedelta(seconds=time)).replace("0000", ""),
        #         inline=False,
        #     )
        #     number += 1

    if(category == 'any%'):
        category = 'anypercent'
    
    cur.execute(f"""
    SELECT user_id, time  FROM {category} ORDER BY time ASC
    """)

    leaderboard = cur.fetchall()

    embed = nextcord.Embed(title=f"Leaderboard for **{category}**", color=nextcord.Color.from_rgb(255, 38, 96))
    number = 0
    for user_id, time in leaderboard:
        number += 1
        user = await bot.fetch_user(int(user_id))
        embed.add_field(
            name = f'{number} - {user}',
            value = str(timedelta(seconds=time)).replace("0000", ""),
            inline = False)

    await ctx.send(embed=embed)

async def get_game():
    api = srcomapi.SpeedrunCom()
    game = api.search(srcomapi.datatypes.Game, {"name": "Celeste"})[0]
    return game

@bot.slash_command()
async def categories(ctx):
    game = await get_game()
    embed = nextcord.Embed(title="Categories", color=nextcord.Color.from_rgb(255, 38, 96))
    for category in game.categories:
        embed.add_field(name=category.name, value=category.weblink)
    await ctx.send(embed=embed)



@bot.slash_command()
async def best_times(ctx, *, category):
    game = await get_game()
    print(game.categories)
    count = -1
    cat_array_num = False
    for i in game.categories:
        print(i)
        count += 1
        if i.name.lower() == category.lower():
            cat_array_num = count
            print(cat_array_num)
            break

    if not cat_array_num:
        await ctx.send("Invalid Category. You can check the categories with /categories")
        return

    record = game.categories[cat_array_num].records[0].runs[0]["run"]
    time = (record.times["primary_t"])
    delta = str(timedelta(seconds=time))
    print(delta)

    embed = nextcord.Embed(title="Best Times", color=nextcord.Color.from_rgb(255, 38, 96))
    embed.add_field(name=game.categories[cat_array_num].name, value=f'Any%: {delta.replace("0000", "")}')
    await ctx.send(embed=embed)


bot.run(os.getenv("TOKEN"))
