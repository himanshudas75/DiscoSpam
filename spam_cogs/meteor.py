#!/usr/bin/python3
import discord
from discord.ext import commands
from spam_modules import meme

class MemeBot(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.command(name='help')
    async def help(self,ctx):
        h=discord.Embed(title='Help',description='Help for Disco Meme')
        h.add_field(name='help',value='Displays this message',inline=False)
        memecommand="""
        Shows a random meme.
        Syntax: ```>meme```
        """
        h.add_field(name='meme',value=memecommand,inline=False)
        await ctx.send(embed=h)

    @commands.command(name='meme',help='Show a random meme')
    async def memes(self,ctx):
        link=meme.getmeme(1)
        emb=discord.Embed()
        emb.set_image(url=link[0])
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(MemeBot(client))