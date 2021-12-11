import os
import requests
from discord.ext import commands
from datetime import date, timedelta, datetime

baseURL = "http://admin.multirest.eu/api/"

def getHelp(*args):
    return "Usa`!multirest [`fcup` / `feup`] [`semana`/`hoje`/`amanha`]`"

#TODO: get prefix from run.py
def invalidArg(*args):
    return getHelp()

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
    days = ['**Segunda**', '**Terça**', '**Quarta**', '**Quinta**', '**Sexta**', '**Sábado**', '**Domingo**']
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