# Imports
import discord
from discord.ext import commands

# Embeds
general = discord.Embed(
    title=":bulb:  General Commands",
    colour = discord.Colour.from_rgb(245, 206, 66)
)
general.add_field(name='\a', value="`ping` : Displays the bot's latency\n\n`changePrefix` : changes the bot's prefix in your server")

music = discord.Embed(
    title=":notes:  Music Commands",
    colour=discord.Colour.from_rgb(51, 153, 255)
)
music.add_field(name='\a', value="`join` : Joins the voice channel you are in\n\n`leave` : Disconnects the bot from a voice channel\n\n`play [query]` : Searches and plays a track with the specified keywords\n\n`pause/stop` : Pauses the current track\n\n`resume` : Resumes playback")

playlist = discord.Embed(
    title=":green_book:  Playlist Commands",
    colour=discord.Colour.from_rgb(51, 204, 51)
)
playlist.add_field(name='\a', value="`playlist` : Displays your playlist\n\n`playlist play` : Starts playing your playlist\n\n`playlist add [query]` : Searches and adds a track with the specified keywords to your playlist\n\n`playlist remove [index]` : Removes the track at the specified position\n\n`playlist shuffle` : Shuffles your playlist")

# Cog
class Help(commands.Cog):
    
    def init(self, bot):
        self.bot = bot

    # Commands
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        await ctx.author.send(embed=general)
        await ctx.author.send(embed=music)
        await ctx.author.send(embed=playlist)

        if isinstance(message.channel, discord.abc.GuildChannel):
            await ctx.send(":bell: You've got mail!")

def setup(bot):
    bot.add_cog(Help(bot))
