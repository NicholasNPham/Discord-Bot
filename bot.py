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

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel. Join a channel first to run this command.")

client.run(BOTTOKEN)

