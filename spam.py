#!/usr/bin/python3
import discord
import os
from discord import channel
from discord.ext import commands
from discord.utils import get
import json
import asyncio
from spam_modules import meme, naughty
from dotenv import load_dotenv

TOKEN=os.getenv('TOKEN')
DISCO_MEME=os.getenv('DISCO_MEME')
DISCO_HENTAI=os.getenv('DISCO_HENTAI')
UPPER_LIMIT=200

intents=discord.Intents().all()
client=commands.Bot(command_prefix='~',intents=intents)
client1=commands.Bot(command_prefix='>',intents=intents)
client2=commands.Bot(command_prefix=':',intents=intents)

client.remove_command('help')
client1.remove_command('help')
client2.remove_command('help')

client.load_extension('spam_cogs.disco')
client1.load_extension('spam_cogs.meteor')
client2.load_extension('spam_cogs.hentai')

@client.event
async def on_ready():
    print('I am online')

def load_guilds():
	global guild_ids
	guild_ids=[]
	with open('not_spammable.json','r') as f:
		guild_ids=json.load(f)
         
@client.command(name='spamall',help='Spam All')
async def spamall(ctx, arg1, arg2=100, arg3=0):
    if arg2>=UPPER_LIMIT:
        emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
        await ctx.send(embed=emb)
        return
    guild_exist = False
    load_guilds()
    if arg1 in guild_ids:
        emb=discord.Embed(title='This guild cannot be spammed',color=0xff0000)
        await ctx.send(embed=emb)
        return
    memelist=meme.getmeme(arg2)
    hentailist=naughty.hentai(arg2,arg3)
    emb=discord.Embed(title='Spam started!',color=0x0000ff)
    await ctx.send(embed=emb)
    for i in range(arg2):
        for guild1, guild2 in zip(client1.guilds,client2.guilds):
            if str(guild1.id) == arg1 and str(guild2.id) == arg1:
                guild_exist = True
                for channel1, channel2 in zip(guild1.channels, guild2.channels):
                    if str(channel1.type) == 'text' and str(channel2.type) == 'text':
                        emb=discord.Embed()
                        e1=get(guild1.roles,name='@everyone')
                        e2=get(guild2.roles,name='@everyone')
                        emb.set_image(url=memelist[i])
                        await channel1.send(f'{e1}')
                        await channel1.send(embed=emb)
                        emb.set_image(url=hentailist[i])
                        await channel2.send(f'{e2}')
                        await channel2.send(embed=emb)
        if not guild_exist:
            emb=discord.Embed(title='Either or Both of Spamming Bots are not in the given guild',color=0xff0000)
            await ctx.send(embed=emb)
            break
    return

@client.command(name='spammeme',help='Spam only memes')
async def spammeme(ctx, arg1, arg2=100):
    if arg2>=UPPER_LIMIT:
        emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
        await ctx.send(embed=emb)
        return
    guild_exist = False
    load_guilds()
    if arg1 in guild_ids:
        emb=discord.Embed(title='This guild cannot be spammed',color=0xff0000)
        await ctx.send(embed=emb)
        return
    memelist=meme.getmeme(arg2)
    emb=discord.Embed(title='Spam started!',color=0x0000ff)
    await ctx.send(embed=emb)
    for i in range(arg2):
        for guild in client1.guilds:
            if str(guild.id) == arg1:
                guild_exist = True
                for channel in guild.channels:
                    if str(channel.type) == 'text':
                        emb=discord.Embed()
                        emb.set_image(url=memelist[i])
                        await channel.send(embed=emb)
        if not guild_exist:
            emb=discord.Embed(title='Meme spamming bot is not in the guild',color=0xff0000)
            await ctx.send(embed=emb)
            break
    return

@client.command(name='spamhentai',help='Spam only hentai')
async def spamhentai(ctx, arg1, arg2=100, arg3=0, arg4=0):
    if arg2>=UPPER_LIMIT:
        emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
        await ctx.send(embed=emb)
        return
    guild_exist = False
    load_guilds()
    if arg1 in guild_ids:
        emb=discord.Embed(title='This guild cannot be spammed',color=0xff0000)
        await ctx.send(embed=emb)
        return
    if not arg2.isnumeric():
        for guild in client2.guilds:
            if str(guild.id) == arg1:
                guild_exist = True
                for user in guild.users:
                    print(user)
                break
    hentailist=naughty.hentai(arg2,arg3)
    emb=discord.Embed(title='Spam started!',color=0x0000ff)
    await ctx.send(embed=emb)
    for i in range(arg2):
        for guild in client2.guilds:
            if str(guild.id) == arg1:
                guild_exist = True
                for channel in guild.channels:
                    if str(channel.type) == 'text':
                        emb=discord.Embed()
                        emb.set_image(url=hentailist[i])
                        await channel.send(embed=emb)
        if not guild_exist:
            emb=discord.Embed(title='Hentai spamming bot is not in the guild',color=0xff0000)
            await ctx.send(embed=emb)
            break
    return

loop=asyncio.get_event_loop()
loop.create_task(client.start(TOKEN))
loop.create_task(client1.start(DISCO_MEME))
loop.create_task(client2.start(DISCO_HENTAI))
loop.run_forever()