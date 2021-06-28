#!/usr/bin/python3
from spam import UPPER_LIMIT
import discord
from discord.ext import commands
import json
from spam_modules import meme, naughty

UPPER_LIMIT = 200

class DiscoBot(commands.Cog):

    def __init__(self,client):
        self.client=client

    def load_guilds(self):
        global guild_ids
        guild_ids=[]
        with open('not_spammable.json','r') as f:
            guild_ids=json.load(f)

    @commands.command(name='help')
    async def help(self,ctx):
        h=discord.Embed(title='Help',description='Help for Disco Bot')
        h.add_field(name='help',value='Displays this message',inline=False)
        text="""
        Spam the specified server with memes and hentai pics.
        *Syntax:* ```~spamall <server_id> <optional: number of pics per category to spam> <optional: is_nsfw>```
        *Note:* 
        0 for sfw, and any other number for nsfw.
        Default number of pics is 100 and 'sfw' is the default hentai mode.
        """
        h.add_field(name='spamall',value=text,inline=False)
        text="""
        Spam the specified server with memes.
        *Syntax:* ```~spammeme <server_id> <optional: number of pics to spam>```
        *Note:* 
        Default number of pics is 100.
        """
        h.add_field(name='spammeme',value=text,inline=False)
        text="""
        Spam the specified server with hentai pics.
        *Syntax:* ```~spamhentai <server_id> <optional: number of pics to spam> <optional: is_nsfw>```
        *Note:* 
        0 for sfw, and any other number for nsfw.
        Default number of pics is 100 and 'sfw' is the default hentai mode.
        """
        h.add_field(name='spamhentai',value=text,inline=False)
        text="""
        Spam the specified user's DM with memes.
        *Syntax:* ```~dspammeme <user_mention> <optional: number of pics to spam>```
        *Note:* 
        Default number of pics is 100.
        """
        h.add_field(name='dspammeme',value=text,inline=False)
        text="""
        Spam the specified user's DM with hentai pics.
        *Syntax:* ```~dspamhentai <user_mention> <optional: number of pics to spam> <optional: is_nsfw>```
        *Note:* 
        0 for sfw, and any other number for nsfw.
        Default number of pics is 100 and 'sfw' is the default hentai mode.
        """
        h.add_field(name='dspamhentai',value=text,inline=False)
        text="""
        Show the non-spammable server list.
        *Syntax:* ```~showns```
        """
        h.add_field(name='showns',value=text,inline=False)
        text="""
        Add a server to the not-spammable list.
        *Syntax:* ```~addns <server_id> <server_name>```
        """
        h.add_field(name='addns',value=text,inline=False)
        text="""
        Remove a server from the non-spammable list.
        *Syntax:* ```~remns <server_id>```
        """
        h.add_field(name='remns',value=text,inline=False)
        await ctx.send(embed=h)
    
    @commands.command(name='showns',help='Show non-spammable guilds')
    async def showns(self,ctx):
        self.load_guilds()
        emb=discord.Embed(title='Non-Spammable Servers',color=0x00ff00)
        for guildid in guild_ids:
            emb.add_field(name=guild_ids[guildid],value=guildid,inline=False)
        await ctx.send(embed=emb)

    @commands.command(name='addns',help='Add a non-spammable server')
    async def addns(self,ctx,servid:int,*,servname):
        self.load_guilds()
        if str(servid) in guild_ids:
            emb=discord.Embed(title='Server ID already added',color=0xff0000)
            await ctx.send(embed=emb)
            return
        emb=discord.Embed(title='Server ID added succesfully',color=0x0000ff)
        await ctx.send(embed=emb)
        guild_ids[str(servid)]=servname
        with open('not_spammable.json','w') as f:
            json.dump(guild_ids,f,indent=4)
    
    @commands.command(name='remns',help='Remove a non-spammable server')
    async def remns(self,ctx,servid:int):
        self.load_guilds()
        if str(servid) not in guild_ids:
            emb=discord.Embed(title='Server ID is not present in non-spammable list',color=0xff0000)
            await ctx.send(embed=emb)
            return
        emb=discord.Embed(title='Server ID successfully removed',color=0x0000ff)
        await ctx.send(embed=emb)
        guild_ids.pop(str(servid))
        with open('not_spammable.json','w') as f:
            json.dump(guild_ids,f,indent=4)
        
    @commands.command(name='dspammeme', help='Spam DMs with memes')
    async def dspammeme(self, ctx, user:discord.User,arg2=100):
        if arg2>=UPPER_LIMIT:
            emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
            await ctx.send(embed=emb)
            return
        memelist=meme.getmeme(arg2)
        emb=discord.Embed(title='Spam started!',color=0x0000ff)
        await ctx.send(embed=emb)
        for i in range(arg2):
            emb=discord.Embed()
            emb.set_image(url=memelist[i])
            await user.send(embed=emb)

    @commands.command(name='dspamhentai', help='Spam DMs with hentai')
    async def dspamhentai(self, ctx, user:discord.User,arg2=100,arg3=0):
        if arg2>=UPPER_LIMIT:
            emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
            await ctx.send(embed=emb)
            return
        hentailist=naughty.hentai(arg2,arg3)
        emb=discord.Embed(title='Spam started!',color=0x0000ff)
        await ctx.send(embed=emb)
        for i in range(arg2):
            emb=discord.Embed()
            emb.set_image(url=hentailist[i])
            await user.send(embed=emb)

def setup(client):
    client.add_cog(DiscoBot(client))