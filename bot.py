import asyncio
import json
import os
import sys
import nextcord
import aiohttp
import aiofiles
from rich import print, console
from dotenv import load_dotenv
from nextcord.ext import commands, tasks

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


class CloseButton(nextcord.ui.View):
    def __init__(self, message: nextcord.Message):
        super().__init__()
        self.message = message

    @nextcord.ui.button(label="🗑️", style=nextcord.ButtonStyle.red)
    async def close_button(
            self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        await self.message.delete()


async def readConfig():
    with open("config.json", "r", encoding="utf8") as jsonfile:
        config = json.loads(jsonfile.read())
        console.log("Config loaded [green]successfully[/green].")
        print(config)
        return config


# On ready, do this.
@bot.event
async def on_ready():
    config = await readConfig()
    if not config["channel_id"]:
        config = await readConfig()
    try:
        channel_id = int(config["channel_id"])
        console.log(f"Channel ID Set to: {channel_id}.")
    except Exception as e:
        console.log(f"[red]Error[/red]: Couldn't read channel id: {e}")
        sys.exit(1)

    print(f"Logged in as {bot.user}.")
    channel = bot.get_channel(channel_id)
    console.log(f"Channel #{channel.name} ({channel.id}) [green]found[/green].")

    # You have to make the message a variable so the ctx.edit() can use it. Without it, it doesn't have the correct
    # context.
    message = await channel.send(
        embed=nextcord.Embed(
            title="The bot has been enabled.", description="Welcome!", color=0x008B02
        )
    )
    await asyncio.sleep(5)
    embed = nextcord.Embed(
        title="Command List:", description="!prioq \n !start", color=0x5300EB
    ).set_footer(
        text="Remember that you can always invoke the command list using !help"
    )
    await message.edit(embed=embed, delete_after=5)


# @bot.event
# async def on_command_error(ctx, error):
#     console.log(f"[red]Error[/red]: {str(error)}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


async def write_list(a_list):
    with open("users.json", "w") as f:
        json.dump(a_list, f)
        print("Done writing JSON data into .json file")


async def read_list():
    # for reading also binary mode is important
    with open("users.json", "r") as fp:
        n_list = json.load(fp)
    return n_list


@bot.command()
async def register(ctx):
    existing_users = await read_list()
    user_id = ctx.author.id
    if user_id not in existing_users:
        existing_users.append(user_id)
        await write_list(existing_users)
        await ctx.send('Registered successfully')
    else:
        await ctx.send("You're already registered")


bot.run(os.getenv("TOKEN"))
