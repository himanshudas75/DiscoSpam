#!/usr/bin/python3
import discord
import os
from discord import channel
from discord.ext import commands
from discord import FFmpegAudio
from discord.player import FFmpegPCMAudio
from discord.utils import get
import json
import asyncio
from spam_modules import meme, naughty
from dotenv import load_dotenv

TOKEN=os.getenv('TOKEN')
DISCO_MEME=os.getenv('DISCO_MEME')
DISCO_HENTAI=os.getenv('DISCO_HENTAI')
UPPER_LIMIT=200
AUDIO_SOURCE = f'{os.getcwd()}/audio/play.mp3'
NOT_SPAM = f'{os.getcwd()}/not_spammable.json'

cl=[]
intents=discord.Intents().all()
client=commands.Bot(command_prefix='~',intents=intents)
cl.append(commands.Bot(command_prefix='>',intents=intents))
cl.append(commands.Bot(command_prefix=':',intents=intents))

client.remove_command('help')
cl[0].remove_command('help')
cl[1].remove_command('help')

client.load_extension('spam_cogs.disco')
cl[0].load_extension('spam_cogs.meteor')
cl[1].load_extension('spam_cogs.hentai')

def load_guilds():
	global guild_ids
	guild_ids=[]
	with open(NOT_SPAM,'r') as f:
		guild_ids=json.load(f)

async def voice_spam(channel,guild,ch):
    vc=discord.utils.get(cl[ch].voice_clients,guild=guild)
    if not vc:
        await channel.connect()
        vc=discord.utils.get(cl[ch].voice_clients,guild=guild)
    if vc.is_playing():
        return
    if vc.is_paused():
        print('Paused')
        vc.resume()
        return
    source=FFmpegPCMAudio(AUDIO_SOURCE)
    vc.play(source)
    return

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
        for guild1, guild2 in zip(cl[0].guilds,cl[1].guilds):
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

@client.command(name='spam',help='Spam only hentai')
async def spam(ctx, arg0, arg1, arg2='100', arg3=0, arg4=0):

    if arg0 == 'm' or arg0 == 'M':
        type_bot = 'Meme'
        ch=0
    elif arg0 == 'h' or arg0 == 'H':
        type_bot = 'Hentai'
        ch=1
    else:
        emb=discord.Embed(title='Please enter either m (meme) or h (hentai)',color=0xff0000)
        await ctx.send(embed=emb)
        return

    load_guilds()
    if arg1 in guild_ids:
        emb=discord.Embed(title='This guild cannot be spammed',color=0xff0000)
        await ctx.send(embed=emb)
        return
    
    guild_exist = False
    for guild in cl[ch].guilds:
        if str(guild.id) == arg1:
            guild_exist = True
            break
    if not guild_exist:
        emb=discord.Embed(title=f'{type_bot} spamming bot is not in the guild',color=0xff0000)
        await ctx.send(embed=emb)
        return

    if not arg2.isnumeric():    #DM Spam another server
        user_exist = False
        for user in guild.members:
            if str(user) == arg2:
                user_exist = True
                break
        if not user_exist:
            emb=discord.Embed(title='User not found in guild',color=0xff0000)
            await ctx.send(embed=emb)
            return
        if arg3>=UPPER_LIMIT:
            emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
            await ctx.send(embed=emb)
            return
        if arg3 == 0:
            arg3 = 100
        if ch == 0:
            li=meme.getmeme(arg3)
        else:
            li=naughty.hentai(arg3,arg4)
        emb=discord.Embed(title='Spam started!',color=0x0000ff)
        await ctx.send(embed=emb)
        for i in range(arg3):
            emb=discord.Embed()
            emb.set_image(url=li[i])
            await user.send(embed=emb)
        return

    arg2 = int(arg2)    #Server Spam
    if arg2>=UPPER_LIMIT:
        emb=discord.Embed(title=f'Please enter a number less than {UPPER_LIMIT}',color=0xff0000)
        await ctx.send(embed=emb)
        return
    if ch == 0:
        li=meme.getmeme(arg2)
    else:
        li=naughty.hentai(arg2,arg3)
    emb=discord.Embed(title='Spam started!',color=0x0000ff)
    await ctx.send(embed=emb)
    for i in range(arg2):
        aud=0
        for channel in guild.channels:
            if str(channel.type) == 'text':
                emb=discord.Embed()
                emb.set_image(url=li[i])
                await channel.send(embed=emb)
            elif aud == 0 and str(channel.type) == 'voice':
                await voice_spam(channel,guild,ch)
                aud+=1
    return

loop=asyncio.get_event_loop()
loop.create_task(client.start(TOKEN))
loop.create_task(cl[0].start(DISCO_MEME))
loop.create_task(cl[1].start(DISCO_HENTAI))
loop.run_forever()