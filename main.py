# Imports
import discord
from discord.ext import commands
import json
import os

# Functions
def get_prefix(bot, message):
    if isinstance(message.channel, discord.abc.PrivateChannel):
        return '.'
    
    else:
        with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

# Initiation
inviteLink = 'https://discord.com/api/oauth2/authorize?client_id=732712093756948579&permissions=8&scope=bot'
bot = commands.Bot(command_prefix=get_prefix, owner_id=402954494406819862)
bot.remove_command('help')


# Events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} | {bot.user.id}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Mostly Working"))

@bot.event
async def on_message(message):
    if "<@!732712093756948579>" in message.content:
        await message.channel.send(f"Hey! My prefix in this server is  `{get_prefix(bot, message)}`")
    
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.' #adds the default '!' prefix to the file

    with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'w') as f: #updates the file
        json.dump(prefixes, f, indent=4)
    
    print("Prefix entry added")

@bot.event
async def on_guild_remove(guild):
    with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    print("Prefix entry removed")


# Admin Commands
@bot.command()
@commands.is_owner()
async def close(ctx): # closes the clients connection to Discord
    await bot.close()
    print('Client connection closed')

@bot.command()
@commands.is_owner()
async def reload(ctx): # reloads all cogs
    for file in os.listdir('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/cogs'):
        if file.endswith('.py'):
            bot.unload_extension(f'cogs.{file[:-3]}')
            bot.load_extension(f'cogs.{file[:-3]}')

@bot.command()
@commands.is_owner()
async def status(ctx, *, text): # changes the bot's status on Discord
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(text))


# Runtime
for file in os.listdir('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/cogs'): # load .py files in cogs folder
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run('TOKEN')
