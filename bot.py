import os
import requests
from requests.api import get
from discord.ext import commands
from datetime import date, timedelta, datetime

PREFIX = os.getenv('PREFIX') or "!"
DISCORD_API_TOKEN = os.getenv('DISCORD_API_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)

baseURL = "http://admin.multirest.eu/api/"

@bot.event # on_ready
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def multirest(ctx, arg="help"):
    arg = arg.lower()
    if arg == 'help':
        await ctx.send(f"{PREFIX}multirest [`semana`/`hoje`/`amanha`]")
    elif arg == "semana":
        await ctx.send(getSemana())
    elif arg == "hoje":
        await ctx.send(getToday())
    elif arg == "amanha":
        await ctx.send(getTomorrow())
    else:
        await ctx.send(f"Argumento inválido. Usa {PREFIX}multirest [`semana`/`hoje`/`amanha`]")


def getSemana():
    r = requests.get(baseURL + 'weekly-menus')

    resposta = r.json()

    fcupJson = resposta[0]
    pratos = fcupJson.get('dishes')
    return parseSemana(pratos)

def getToday():
    today = date.today()
    dayNum = today.weekday()
    today = today.strftime("%Y-%m-%d")
    url = baseURL + "daily-menus?date=" + today + "&institution_id=1"
    r = requests.get(url)

    resposta = r.json()
    resposta = resposta[0]
    pratos = resposta.get('dishes')
    if pratos:
        return getDayByIndex(dayNum) + "\n\n" + parseDia(pratos)
    else:
        return getDayByIndex(dayNum) + "\n\n" + "Não há pratos para hoje"

def getTomorrow():
    tomorrow = date.today() + timedelta(days=1)
    dayNum = tomorrow.weekday()
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    url = baseURL + "daily-menus?date=" + tomorrow + "&institution_id=1"
    r = requests.get(url)

    resposta = r.json()
    resposta = resposta[0]
    pratos = resposta.get('dishes')
    if pratos:
        return getDayByIndex(dayNum) + "\n\n" + parseDia(pratos)
    else:
        return getDayByIndex(dayNum) + "\n\n" + "Não há pratos para amanhã"
    pass

def parseDia(dia):
    var = ""
    for i in range(0,4):
        var += "__" + dia[i]['type_name'] + "__" + " : " + dia[i]['name'] + '\n'
    return var

def getDayByIndex(day):
    days = ['**Segunda**', '**Terça**', '**Quarta**', '**Quinta**', '**Sexta**']
    return days[day]

def parseSemana(semana):
    var = ""
    for i in range(1,6):
        dia = semana.get(str(i))
        if dia:
            var += getDayByIndex(i - 1) + "\n\n" + parseDia(dia) + '\n'
        else:
            var += getDayByIndex(i-1) + " - Feriado" + '\n\n'
    return var

bot.run(DISCORD_API_TOKEN)
