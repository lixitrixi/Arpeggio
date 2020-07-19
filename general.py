# Imports
import discord
from discord.ext import commands
import json

# Cog
class General(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! ({round(self.bot.latency*1000)}ms)')
    
    @commands.command(aliases=['change_prefix'])
    @commands.has_permissions(administrator=True)
    async def changePrefix(self, ctx, prefix):
        
        with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('/Users/felixleitner/Desktop/Discord_Bots/MusicBot/clientData/prefixes.json', 'w') as f: #updates the file
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Server prefix was changed to  `{prefix}`")

    # Errors
    @changePrefix.error
    async def changePrefix_error(self, ctx, error):
        
        if isinstance(error, commands.MissingPermissions): #if user does not have admin perms
            await ctx.send("Error: Administrator permissions are recquired to use this command")
    
        if isinstance(error, commands.MissingRequiredArgument): #if a prefix is not given
            await ctx.send("`.prefix [new prefix]`\nError: Missing required argument")

def setup(bot):
    bot.add_cog(General(bot))
