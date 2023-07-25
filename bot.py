import discord
from discord.ext import commands

# API Discord Token
from apikeys import *

client = commands.Bot(command_prefix='.', intents = discord.Intents.all())       

@client.event
async def on_ready():
    print('Bot is Online.')
    print('-------------------')

@client.command()
async def hello(ctx):
    await ctx.send('This is Bot Responding.')

client.run(BOTTOKEN)

