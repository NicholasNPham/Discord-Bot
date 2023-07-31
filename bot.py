import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions

# API Discord Token
from apikeys import *

# General Setup
intents = discord.Intents.all()
intents.members = True

# Wave File To Start
wav_file = 'eyes.wav'

# Queue Dictionary
queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

"""
Client Events
"""

client = commands.Bot(command_prefix='.', intents=intents)       

@client.event
async def on_ready():
    print('Bot is Online.')
    print('-------------------')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1092278186886303858)
    await channel.send("Hello " + str(member))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1092278186886303858)
    await channel.send("Goodbye " + str(member))

@client.event
async def on_message(message):

    if message.content == 'hi':
        await message.delete()
        await message.channel.send("Dont Say Hi")
    await client.process_commands(message)

@client.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permission to run this command.")

"""
Client Commands
"""

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('eyes.wav')
        player = voice.play(source)
        await ctx.send("Now Playing " + wav_file)
    else:
        await ctx.send("You are not in a voice channel. Join a channel first to run this command.")

@client.command()
async def hello(ctx):
    await ctx.send('This is Bot Responding.')

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the Voice Channel.")
    else:
        await ctx.send("Not in voice channel.")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No Song is Playing.")
        
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Song is Playing")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
    await ctx.send("Song " + str(song) + ' is Playing')
 
@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send(str(song) + ' Added to Queue')

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@client.command()
async def embed(ctx):
    embed = discord.Embed(
        title='GitHub',
        url='https://github.com/NicholasNPham', 
        description="My Profile", color=0xa8a7a7)
    
    embed.set_author(
        name="Nicholas Pham",
        url="https://github.com/NicholasNPham/FlaskAppTrade/commits?author=NicholasNPham",
        icon_url="https://avatars.githubusercontent.com/u/132528074?s=400&u=292ac87004412c2c0a34b319e84b7f82e4a6dcf7&v=4")

    embed.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2021/05/GitHub-logo.png")

    embed.add_field(
        name="Repositories",
        value="Check out all the repositories made under this GitHub profile.",
        inline=True)

    embed.add_field(
        name="Current Project",
        value="Trading Website made with Flask & TradingView_TA Packages.",
        inline=True)

    await ctx.send(embed=embed)

# Client Errors

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Dont have Permissions to kick people!")

client.run(BOTTOKEN)

