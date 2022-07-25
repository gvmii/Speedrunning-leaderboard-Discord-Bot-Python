from nextcord.ext import commands


@commands.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.display_name}.")
