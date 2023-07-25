import discord
from discord.ext import commands

intents = discord.Intents.default()

client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('Bot is Ready.')

client.run('Token Example')