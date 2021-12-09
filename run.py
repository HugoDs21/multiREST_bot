import os
import requests
from discord.ext import commands
from datetime import date, timedelta, datetime

PREFIX = os.getenv('PREFIX') or "!"
DISCORD_API_TOKEN = os.getenv('DISCORD_API_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)

baseURL = "http://admin.multirest.eu/api/"

instituicoes = {"fcup": 0, "feup": 2}

@bot.event # on_ready
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def multirest(ctx, arg1 = "fcup", arg2 = "help"):
    arg1 = arg1.lower()
    arg2 = arg2.lower()
    id = instituicoes.get(arg1)
    if id == 0:
        if arg2 == 'help':
            await help(ctx)
        elif arg2 == "semana":
            await ctx.send(getSemana(id, arg1))
        elif arg2 == "hoje":
            await ctx.send(getToday(id, arg1))
        elif arg2 == "amanha":
            await ctx.send(getTomorrow(id, arg1))
        else:
            await ctx.send(f"Argumento inválido. Usa {PREFIX}multirest [`semana`/`hoje`/`amanha`]")
    elif id == 2:
        if arg2 == 'help':
            await help(ctx)
        elif arg2 == "semana":
            await ctx.send(getSemana(id, arg1))
        elif arg2 == "hoje":
            await ctx.send(getToday(id+1, arg1))
        elif arg2 == "amanha":
            await ctx.send(getTomorrow(id+1, arg1))
        else:
            await ctx.send(f"Argumento inválido. Usa {PREFIX}multirest [`semana`/`hoje`/`amanha`]")
    else:
        await ctx.send(f"Argumento inválido. Usa {PREFIX}multirest [`semana`/`hoje`/`amanha`]")

async def help(ctx):
    await ctx.send("Use `!multirest [`fcup` / `feup`] [`semana`/`hoje`/`amanha`]`")

def getSemana(id, arg1):
    r = requests.get(baseURL + 'weekly-menus')

    resposta = r.json()

    respostaJson = resposta[id]
    pratos = respostaJson.get('dishes')
    return "__**" + arg1.upper() + "**__\n\n" + parseSemana(pratos)

def getToday(id, arg1):
    today = date.today()
    dayNum = today.weekday()
    today = today.strftime("%Y-%m-%d")
    url = f"{baseURL}daily-menus?date={today}&institution_id={id}"
    r = requests.get(url)

    resposta = r.json()
    resposta = resposta[0]
    pratos = resposta.get('dishes')
    if pratos:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + parseDia(pratos)
    else:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + "Não há pratos para hoje"

def getTomorrow(id, arg1):
    tomorrow = date.today() + timedelta(days=1)
    dayNum = tomorrow.weekday()
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    url = f"{baseURL}daily-menus?date={tomorrow}&institution_id={id}"
    r = requests.get(url)

    resposta = r.json()
    resposta = resposta[0]
    pratos = resposta.get('dishes')
    if pratos:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + parseDia(pratos)
    else:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + "Não há pratos para amanhã"
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
