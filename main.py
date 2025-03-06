from asyncio import run
from os import listdir

import discord as dc
from discord.ext import commands


# client / bot
client: commands.Bot = commands.Bot(
    command_prefix='aprefix',
    description="a description",
    intents=dc.Intents.all()
)
client.remove_command('help')


async def load() -> None :
    """
    load cogs
    """

    for file in listdir('./cogs') :
        if file.endswith(".py") :
            await client.load_extension(f'cogs.{file[:-3]}')


@client.hybrid_command(hidden=True)
async def sync(ctx: commands.Context) -> None :
    """
    sync commands
    """

    # authorized users only
    if ctx.author.id not in [''] :
        return

    await client.tree.sync()
    await client.wait_until_ready()
    await ctx.send('Done !', ephemeral=True)


async def amain() -> None :
    await load()
    await client.start('')


run(amain())
