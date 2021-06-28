#!/usr/bin/python3
import requests
import json
import threading

url='https://meme-api.herokuapp.com/gimme/'
out=[]

def memethread(n):
    global out
    u=f'{url}{n}'
    r=requests.get(u)
    json_data=json.loads(r.text)
    for j in range(n):
        image=json_data['memes'][j]['url']
        out.append(image)

def getmeme(n):
    threads=[]
    global out
    rem=n%50
    div=n//50
    for i in range(div):
        threads.append(threading.Thread(target=memethread, args=(50,)))

    if rem:
        threads.append(threading.Thread(target=memethread, args=(rem,)))
    
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()

    return out