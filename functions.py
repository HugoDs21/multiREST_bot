import os
import requests
from discord.ext import commands
from datetime import date, timedelta, datetime

baseURL = "http://admin.multirest.eu/api/"

def getHelp(*args):
    return "Usa`!multirest [`fcup` / `feup`] [`semana`/`hoje`/`amanha`]`"

def invalidArg(*args):
    return getHelp()

def getWeek(id, arg1):
    r = requests.get(baseURL + 'weekly-menus')

    res = r.json()

    resJson = res[id]
    dishes = resJson.get('dishes')
    return "__**" + arg1.upper() + "**__\n\n" + parseWeek(dishes)

def getToday(id, arg1):
    if arg1 == "feup":
        id += 1
    
    today = date.today()
    dayNum = today.weekday()
    today = today.strftime("%Y-%m-%d")
    url = f"{baseURL}daily-menus?date={today}&institution_id={id}"
    r = requests.get(url)

    res = r.json()
    res = res[0]
    dishes = res.get('dishes')
    if dishes:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + parseDay(dishes)
    else:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + "Não há dishes para hoje"

def getTomorrow(id, arg1):
    if arg1 == "feup":
        id += 1
    
    tomorrow = date.today() + timedelta(days=1)
    dayNum = tomorrow.weekday()
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    url = f"{baseURL}daily-menus?date={tomorrow}&institution_id={id}"
    r = requests.get(url)

    res = r.json()
    res = res[0]
    dishes = res.get('dishes')
    if dishes:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + parseDay(dishes)
    else:
        return "__**" + arg1.upper() + "**__\n\n" + getDayByIndex(dayNum) + "\n\n" + "Não há dishes para amanhã"
    pass

def parseDay(day):
    var = ""
    for i in range(0,4):
        var += "__" + day[i]['type_name'] + "__" + " : " + day[i]['name'] + '\n'
    return var

def getDayByIndex(day):
    days = ['**Segunda**', '**Terça**', '**Quarta**', '**Quinta**', '**Sexta**', '**Sábado**', '**Domingo**']
    return days[day]

def parseWeek(semana):
    var = ""
    for i in range(1,6):
        day = semana.get(str(i))
        if day:
            var += getDayByIndex(i - 1) + "\n\n" + parseDay(day) + '\n'
        else:
            var += getDayByIndex(i-1) + " - Feriado" + '\n\n'
    return var