# Bot Discord version: BETA

import os
import sys
import json
import time
import asyncio
import discord
import datetime
import requests
import wikipedia

from discord import *
from Lib.Color import *
from keep_alive import keep_alive
from discord.ext import commands
from Lib.OpenVar import *

default_intents = discord.Intents.default()
default_intents.members = True
client = commands.Bot(command_prefix= "//", help_command=None, intents=default_intents)

dict_image = {}

HELP_ISS = """__**HELP ISS**__

**Description**
La commande **ISS** permet d'avoir des information sur cette dernière.

**Syntaxe**
``ISS󠀮 [/h] [/t] [/p] [/m] [/i]``

"""

HELP_PING = """__**HELP PING**__

**Description**
La commande **ping** permet de savoir si le bot est connecté.

**Syntaxe**
``ping``

"""

HELP_INFO = """__**HELP INFO**__

**Description**
La commande **info** permet d'avoir des information sur le bot et le serveur Discord.

**Syntaxe**
``info [/h] [/m <@pseudo>󠀮] [/bot] [/server]``

"""


def error(commande):
    return discord.Embed(description=f"""__**ERREUR**__\n\n``{commande}`` n’est pas reconnu en tant que commande interne ou externe.\nTapez ``//help`` pour voir toutes les commandes disponible ou tapez\n``//help <commande>`` pour voir le manuel d'utilisation d'une commande.""", color=color.red)


def date(option="DD/MM/YYYY"):
    second = minute = hour = month = day = ""
    date = datetime.datetime.now()

    if date.day <= 10:
        day = "0" + str(date.day)
    elif date.day > 10:
        day = str(date.day)
    if date.month <= 10:
        month = "0" + str(date.month)
    elif date.month > 10:
        month = str(date.month)
    if date.hour <= 10:
        hour = "0" + str(date.hour)
    elif date.hour > 10:
        hour = str(date.hour)
    if date.minute <= 10:
        minute = "0" + str(date.minute)
    elif date.minute > 10:
        minute = str(date.minute)
    if date.second <= 10:
        second = "0" + str(date.second)
    elif date.second > 10:
        second = str(date.second)
    
    return option.replace("DD", day).replace("MM", month).replace("YYYY", str(date.year)).replace("hh", hour).replace("mm", minute).replace("ss", second)


@client.event
async def on_ready():
    global dict_image
    print("\nConnecter à {0.user}\n".format(client))

    dict_channel = {}
    for guild in client.guilds:
        if guild.id == 836989044100431892:
            for channel in guild.text_channels:
                dict_channel[str(channel.name)] = channel.id
    dict_image = {}
    for values in dict_channel.values():
        channel = client.get_channel(values)
        dict_image[str(channel.name)] = {}
        async for message in channel.history(limit=None):
            attachment = message.attachments[0]
            nom = str(attachment.filename).split(".")
            nom.remove(nom[len(nom)-1])
            dict_image[str(channel.name)][".".join(nom)] = str(attachment.url)
    open("Temp/Data/ImageDictionnaire.py", "w").write(str(dict_image).replace("', '", "',\n'"))

ListSlash = ["///"]
for i in range(1, 100):
    ListSlash.append(str(ListSlash[i-1]) + "/")
@client.command(aliases=ListSlash)
async def _EasterEgg(ctx):
    await ctx.send("🤬 ARRETE DE M'APPELER")


@client.command(aliases=["set", "setting", "configuration"])
async def config(ctx, command=None, option=None, value=None):
    if command == "log":
        if option == "channel" or option == "salon":
            if value != None:
                if "<#" in value:
                    tmp = string("Temp/Data/Configuration.ini", "channel_log")
                    value = str(value.replace("<#", "").replace(">", ""))
                    tmp3 = str(open("Temp/Data/Configuration.ini", "r").read())
                    open("Temp/Data/Configuration.ini", "w").write(tmp3.replace(tmp, value))
                    channel = client.get_channel(int(value))
                    embed = discord.Embed(description=f"__**LOG CHANNEL**__\n\nLes logs seront écrits dans le salon :```Elm\nID = {channel.id}\nName = {channel.name}```", color=color.green)
                else:
                    await ctx.send(embed=error(value))
            else:
                channel = client.get_channel(integer("Temp/Data/Configuration.ini", "channel_log"))
                embed = discord.Embed(description=f"__**LOG CHANNEL**__\n\n```Elm\nID = {channel.id}\nName = {channel.name}```", color=color.blue)
    embed.set_thumbnail(url=dict_image["logo"]["settings"])
    await ctx.send(embed=embed)

@client.event
async def on_message_delete(message):
    channel = client.get_channel(integer("Temp/Data/Configuration.ini", "channel_log"))
    if message.author == client.user:
        return
    if 1 == 1:
        embed = discord.Embed(description="__**MESSAGE SUPRIMMÉ**__\n󠀮 ", color=color.red)
        embed.add_field(name="Auteur :", value="<@" + str(message.author.id) + ">", inline=False)
        if str(message.embeds) == "[]": embed.add_field(name="Contenant :", value=str(message.content), inline=False)
        else: embed.add_field(name="Contenant :", value=str(message.embeds), inline=False)
        embed.add_field(name="Salon :", value=f"```Elm\nID = {message.channel.id}\nName = {message.channel}```", inline=False)
        #embed.add_field(name="Supprimé par :", value="<@" + str(deleter.id) + ">", inline=False)
        embed.add_field(name="Date :", value=date("DD/MM/YYYY - hh:mm:ss"), inline=False)
        embed.set_thumbnail(url=dict_image["logo"]["message_supprime"])
        await channel.send(embed=embed)
    else:
        print("[-] Erreur : on_message_delete")


@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send(embed=discord.Embed(description=f"**Latence :** {round(float(client.latency * 1000))} ms" , color=0x2f3136).set_author(name="Je suis en ligne"))


@client.command()
async def info(ctx, user_id=None):
    try:
        if "<@!" in user_id.lower():
            member = client.get_user(int(str(user_id).replace("<@!", "").replace(">", "")))
            embed=discord.Embed(description=f"__**INFO MEMBRE**__\n\n**Name : **{member.name}\n**Discriminateur : **{member.discriminator}\n**Identifiant : **{member.id}", color=color.faketransparent)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
    except:
        embed=discord.Embed(description=f"**ERREUR**\n\ninfo <user> → Information sur un membre du serveur" , color=color.red)
        await ctx.send(embed=embed)


@client.command(aliases=["iss"])
async def ISS(ctx, option=None):
    if "/t" in option:
        PositionTracker = requests.get("http://api.open-notify.org/iss-now.json").json()
        embed=discord.Embed(description=f"__**ISS Position**__\n\n**Latitude : **{str(PositionTracker['iss_position']['latitude'])}\n**Longitude : **{str(PositionTracker['iss_position']['longitude'])}" , color=color.blue)
        embed.set_thumbnail(url=dict_image["space"]["ISS_logo"])
        await ctx.send(embed=embed)

    if "/p" in option:
      await ctx.send("Bientôt Disponible")

    if "/i" in option:
      await ctx.send("Bientôt Disponible")

    if "/m" in option:
      await ctx.send("Bientôt Disponible")

    if "/h" in option:
        await help(ctx=ctx, option="ISS")

    else:
        await ctx.send(embed=error("ISS " + str(option)))

@client.command()
async def help(ctx, option=None):
    if option==None:
        embed = discord.Embed(color=color.yellow, description="__**HELP**__\n\nBOT Discord programmer son python par <@399969976972214282>.\nSi vous rencontrez un problème ou si vous avez des suggestions contactez-moi.")
        embed.add_field(name="Commande :󠀮󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 󠀮 ", value="**ISS󠀮**\n**NASA**\n**info  <@pseudo>󠀮**\n**ping󠀮**\n**help {commande}**")
        embed.add_field(name="Description :", value="Information sur l'ISS\nInformation sur nasa\nInformation sur un membre du serveur\nSatut et latence du bot\nManuel d'utilisation de la commande en question")
        await ctx.send(embed=embed)

    elif option=="ISS":
        embed = discord.Embed(color=color.yellow, description=HELP_ISS)
        embed.add_field(name="Commande :󠀮󠀮", value="**/h**\n**/t**\n**/p**\n**/m**\n**/i**")
        embed.add_field(name="Description :", value="Affiche ce message\nPistion de l'ISS\nPhoto\nÉquipage\nInformation")
        await ctx.send(embed=embed)

    elif option=="info":
        await ctx.send(embed=discord.Embed(color=color.yellow, description="__**HELP NASA**__\n\nBientôt Disponible"))

    elif option=="ping":
      await ctx.send(embed=discord.Embed(color=color.yellow, description=HELP_PING))


@client.command()
async def upload(ctx, salon : str, *, nom=""):
    global dict_image
    Channel = []
    dict_channel = {}
    for guild in client.guilds:
        if guild.id == 836989044100431892:
            for channel in guild.text_channels:
                dict_channel[str(channel.name)] = channel.id
    channel = client.get_channel(dict_channel[salon])
    for attachment in ctx.message.attachments:
        if nom == "":
            tmp = str(attachment.filename).split(".")
            tmp.remove(tmp[len(tmp)-1])
            nom = ".".join(tmp)
        await attachment.save(f"Temp/Image/{attachment.filename}")
        attachment = ctx.message.attachments[0]
        tmp = str(attachment.filename).split(".")
        nom = nom.replace(" ", "_") + "." + tmp[len(tmp)-1]
        os.rename(f"Temp/Image/{attachment.filename}", f"Temp/Image/{nom}")
        await channel.send(file=discord.File(f"Temp/Image/{nom}"))
        os.remove(f"Temp/Image/{nom}")
    IgnoreDelete = True
    await ctx.message.delete()
    await ctx.send(f"L'image **{nom}** a été téléversé dans le salon **{str(channel.name)}**")

    dict_channel = {}
    for guild in client.guilds:
        if guild.id == 836989044100431892:
            for channel in guild.text_channels:
                dict_channel[str(channel.name)] = channel.id
    dict_image = {}
    for values in dict_channel.values():
        channel = client.get_channel(values)
        dict_image[str(channel.name)] = {}
        async for message in channel.history(limit=None):
            attachment = message.attachments[0]
            nom = str(attachment.filename).split(".")
            nom.remove(nom[len(nom)-1])
            dict_image[str(channel.name)][".".join(nom)] = str(attachment.url)
    open("Temp/Data/ImageDictionnaire.py", "w").write(str(dict_image).replace("', '", "',\n'"))


@client.command()
async def scan_manga(ctx, enter_name, enter_chap=1, page2=1):
  global ctxduscan, nom, ch, page
  ctxduscan = ctx
  nom = enter_name
  ch = enter_chap
  page = page2
  if page < 10:
    url = f"https://lelscans.net/mangas/{nom}/{ch}/0{page}.jpg"
  else:
    url = f"https://lelscans.net/mangas/{nom}/{ch}/{page}.jpg"
  if requests.get(url).status_code == 404:
    listURL = url.split(".")
    del listURL[len(listURL)-1]
    listURL.append("png")
    url = ".".join(listURL)
    if requests.get(url).status_code == 404:
      await ctx.send("Erreur:\nSoit il s'agit du nom du manga soit le manga ou chapitres n'est pas disponible")
  MessageScan = await ctx.send(url)
  await MessageScan.add_reaction(":arrow_backward:")
  await MessageScan.add_reaction(":arrow_forward:")

@client.command()
async def test(ctx):
		os.system("python 'Sherlock/sherlock/sherlock.py' test")

@client.command()
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount + 1)
    message = await ctx.channel.send("message(s) ont été suprimmé.")
    time.sleep(3)
    await message.delete(message)

keep_alive()
client.run(os.environ['Token'])