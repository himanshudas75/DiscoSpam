#!/usr/bin/python3
import hmtai
import random

nsfwlist=['ass','bdsm','cum','manga','femdom','hentai','masturbation','ero','orgy','yuri','pantsu','glasses','cuckold','blowjob','foot','thighs','vagina','ahegao','uniform','gangbang','tentacles','gif','nsfwNeko','nsfwMobileWallpaper','zettaiRyouiki']
sfwlist=['wallpaper','mobileWallpaper','neko','jahy']

def hentai(number, nsfw):
	if nsfw:
		category=random.choice(nsfwlist)
	else:
		category=random.choice(sfwlist)

	check=f"{hmtai.useHM('v2',category)}"
	if 'nothing' in check:
		hentai(number, nsfw)
	li=[]
	for i in range(number):
		li.append(f"{hmtai.useHM('v2',category)}")
	return li