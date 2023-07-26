import discord
from discord.ext import commands

# API Discord Token
from apikeys import *

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)       

@client.event
async def on_ready():
    print('Bot is Online.')
    print('-------------------')

@client.command()
async def hello(ctx):
    await ctx.send('This is Bot Responding.')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1092278186886303858)
    await channel.send("Hello " + str(member))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1092278186886303858)
    await channel.send("Goodbye " + str(member))

client.run(BOTTOKEN)

