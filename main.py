import discord
import os
import requests
import json
import random
from itertools import combinations
from replit import db
from keep_alive import keep_alive
def power(player):
   return int(player)
def tpower(team):
    tp=0
    for i in team:
        tp+=power(i[1])
    return tp
def powerdiff(team1,team2):
    diff=abs(tpower(team1)-tpower(team2))
    return diff

def balance(players):
    perteam=int(len(players)/2)

    comb = combinations(players, perteam)

    min=1000
    team1=[]
    team2=[]
    balteams=[]
    balteam = []
    c=0
    for i in comb:
        c=c+1
        t1=i
        t2= [p for p in players if p not in t1]

        diff=powerdiff(t1,t2)
        if diff<min:
            min=powerdiff(t1,t2)
            team1=t1
            team2=t2
            balteam.clear()
            balteam.append(t1[:])
            balteam.append(t2[:])
            balteams.clear()
            balteams.append(balteam[:])

        elif diff==min:
            balteam.clear()
            balteam.append(t1[:])
            balteam.append(t2[:])
            balteams.append(balteam[:])
    return balteams
client = discord.Client()



if "responding" not in db.keys():
  db["responding"] = True


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game("!bhelp"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!bhelp'):
    str2='Enter the players and their ranks in following format: \n'
    str2=str2+"!balance <player1name>,<player1rank>;<player2name>,<player2rank>; etc..\n"
    str2=str2+"You must enter even number of players(It will make 2 teams) and rank should be a number.\n"

    await message.channel.send(str2)
  if message.content.startswith("!balance"):
    str1=message.content.split("!balance ",1)[1]
    x = []
    players = []
    for i in str1.split(';'):
      x.clear()
      for j in i.split(','):
        x.append(j)
      players.append(x[:])
    balteams = balance(players)
    selectedteam = random.choice(balteams)
    reply="Team 1:\n"
    for i in selectedteam[0]:
        reply=reply+" "+i[0]
    reply=reply+'\n'+"Total Power: "+str(tpower(selectedteam[0]))
    reply=reply+"\n----------------------------------\nTeam 2:\n"
    for i in selectedteam[1]:
        reply=reply+" "+i[1]
    reply=reply+'\n'+"Total Power: "+str(tpower(selectedteam[1]))

    await message.channel.send(reply)
  msg = message.content
  


keep_alive()
client.run(os.getenv('TOKEN'))