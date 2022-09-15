import json
import os
import sys
from datetime import datetime
import aiofiles
import discord
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
    async with aiofiles.open("config.json", mode="r", encoding="utf8") as jsonfile:
        contents = await jsonfile.read()
    config = json.loads(contents)
    console.log("Config loaded [green]successfully[/green].")
    print(config)
    return config


# On ready, do this.
@bot.event
async def on_ready():
    config = await read_config()
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
    console.log(f"Channel #{channel.name} ({channel.id}) [green]found[/green].")


# @bot.event
# async def on_command_error(ctx, error):
#     console.log(f"[red]Error[/red]: {str(error)}")


@bot.command()
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


async def validate_time(time):
    # This might be slow because try excepts are slow in Python, but whatever.
    # TODO: Make this a bit more efficient
    try:
        validated_time = datetime.strptime(time, '%H:%M:%S.%f').time()
    except ValueError:
        return ValueError
    return validated_time


@bot.command()
async def register(ctx):
    existing_users = await read_list('users.json')
    user_id = ctx.author.id
    if user_id not in existing_users:
        existing_users.append(user_id)
        await write_to_file(existing_users, 'users.json')
        await ctx.send('Registered successfully')
    else:
        await ctx.send("You're already registered")


@bot.command()
async def favorite_song(ctx, song):
    loaded_users = await read_list('user_songs.json')
    user_id = ctx.author.id
    # if user_id in loaded_users:

    song_to_write = {user_id: song}
    loaded_users.update(song_to_write)
    print(loaded_users)
    await write_to_file(loaded_users, 'user_songs.json')


@bot.command()
async def register_score(ctx, mode: str, time: str):
    user_id = ctx.author.id
    loaded_file = await read_dict('times.json')

    # TODO: Fix this jank thing
    validated_time = await validate_time(time)
    try:
        formatted_time = validated_time.strftime('%H:%M:%S.%f')
    except AttributeError:
        await ctx.send('Please write your time in the following format: H:M:S:ms')

    else:
        writing_template = {user_id: {mode: formatted_time}}
        print(loaded_file)
        loaded_file.update(writing_template)
        await write_to_file(loaded_file, 'times.json')


@bot.command()
async def personal_best(ctx, mode: str, user: discord.Member = None):
    user_id = ctx.author.id
    loaded_file = await read_dict('times.json')

    user = user or ctx.author

    if user.id in loaded_file:
        pb = loaded_file[user_id].get(mode)
        await ctx.send(f"{user.mention}'s {mode} time is {pb}")


bot.run(os.getenv("TOKEN"))
