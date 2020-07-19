# Imports
import discord
from discord.ext import commands
import wavelink

# Functions


# Cog
class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='0.0.0.0',
                                              port=2333,
                                              rest_uri='http://0.0.0.0:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='us_central')

    @commands.command(aliases=['connect'])
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f':satellite:  Connecting to **{channel.name}**')
        await player.connect(channel.id)
    
    @commands.command()
    async def leave(self, ctx, *, channel: discord.VoiceChannel=None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        await player.destroy()

    @commands.command()
    async def play(self, ctx, *, query: str):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.join)
        
        await ctx.send(f":mag_right:  Searching  `{query}`")
        
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        await ctx.send(f':cd:  Playing **{str(tracks[0])}**')
        await player.play(tracks[0])
    
    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        
        if ctx.author.voice.channel.id == player.channel_id:
            await player.set_pause(True)
            await ctx.message.add_reaction('⏸')
        
        else:
            await ctx.send('You must be in the same channel as the bot to use this command!')
    
    @commands.command()
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        
        if ctx.author.voice.channel.id == player.channel_id:
            await player.set_pause(False)
            await ctx.message.add_reaction('▶')
        
        else:
            await ctx.send('You must be in the same channel as the bot to use this command!')
        


def setup(bot):
    bot.add_cog(Music(bot))
