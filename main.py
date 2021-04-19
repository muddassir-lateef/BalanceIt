import discord
import os
import requests
import json
import random
from itertools import combinations
from replit import db
from keep_alive import keep_alive
playersdata={}
def store(str1):
  tplayers = str1.split(',')
  tplayers[0]=tplayers[0].replace(" ","")
  playersdata.update({tplayers[0]:int(tplayers[1])})
 # playersdata[str(tplayers[0])] =int[tplayers[1]]
def leaderboard():
  tstr=""
  sdata=sorted(playersdata.items(), key=lambda x: x[1], reverse=True)
  n1=1
  for i in sdata:
    tstr=tstr+"\n"+str(n1)+") "+i[0]+"    "+str(i[1])
    n1=n1+1
  return tstr
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
    str2='Bot Commands: \n'
    str2=str2+"!power <playerdiscordtag>,<playerpower> to associate power for that player\n"
    str2=str2+"!ranking shows the current ranking and leaderboard of registered players.\n"
    str2=str2+"!balance <player1discordtag> <player2discordtag> <player3discordtag> <player4discordtag>\n"
    str2=str2+"Note that for !balance the player must be registered and even number of players must be entered.If there are more than one possible balanced teams then running the !balance once more will randomly give another balanced team.\n"


    await message.channel.send(str2)
  if message.content.startswith("!power"):
    str1=message.content.split("!power ",1)[1]
    store(str1)
    await message.channel.send("Power level stored successfully!")
  if message.content.startswith("!ranking"):
    await message.channel.send(leaderboard())
  if message.content.startswith("!balance"):
  

      str1=message.content.split("!balance ",1)[1]
     
      str1=str1.replace("<", "")
      str1=str1.replace(">", "")      
      players = []



      for i in str1.split(" "):
        temp=i
        stemp="<"+temp+">"

        list=[]
        list.append(stemp)
        list.append(playersdata[stemp])
        players.append(list[:])
      balteams = balance(players)
      selectedteam = random.choice(balteams)
      reply="Team 1:\n"
      for i in selectedteam[0]:
          reply=reply+" "+i[0]
      reply=reply+'\n'+"Total Power: "+str(tpower(selectedteam[0]))
      reply=reply+"\n----------------------------------\nTeam 2:\n"
      for i in selectedteam[1]:
          reply=reply+" "+i[0]
      reply=reply+'\n'+"Total Power: "+str(tpower(selectedteam[1]))

      await message.channel.send(reply)
  msg = message.content
  


keep_alive()
client.run(os.getenv('TOKEN'))
