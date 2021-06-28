#!/usr/bin/python3
import discord
from discord.ext import commands
from spam_modules import naughty

class HentaiBot(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.command(name='help')
    async def help(self,ctx):
        h=discord.Embed(title='Help',description='Help for Disco Hentai')
        h.add_field(name='help',value='Displays this message',inline=False)
        hentaicommand="""
        Shows a random hentai pic.
        Syntax: ```:hentai <optional: if_nsfw>```
        if_nsfw -> Enter 0 for sfw, any other number for nsfw (By default, the option is sfw)
        """
        h.add_field(name='hentai',value=hentaicommand,inline=False)
        await ctx.send(embed=h)

    @commands.command(name='hentai',help='Show a random hentai')
    async def hentai(self,ctx,arg=0):
        link=naughty.hentai(1,arg)
        emb=discord.Embed()
        emb.set_image(url=link[0])
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(HentaiBot(client))