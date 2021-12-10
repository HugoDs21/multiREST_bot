import os
import requests
import functions as func
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
async def multirest(ctx, *args):
    arg1 = arg1.lower()
    arg2 = arg2.lower()
    id = instituicoes.get(arg1)
    if id == 0:
        if arg2 == 'help':
            await func.getHelp(ctx)
        elif arg2 == "semana":
            await ctx.send(func.getSemana(id, arg1))
        elif arg2 == "hoje":
            await ctx.send(func.getToday(id, arg1))
        elif arg2 == "amanha":
            await ctx.send(func.getTomorrow(id, arg1))
        else:
            await func.invalidArg(ctx)
    elif id == 2:
        if arg2 == 'help':
            await getHelp(ctx)
        elif arg2 == "semana":
            await ctx.send(func.getSemana(id, arg1))
        elif arg2 == "hoje":
            await ctx.send(func.getToday(id+1, arg1))
        elif arg2 == "amanha":
            await ctx.send(func.getTomorrow(id+1, arg1))
        else:
            await func.invalidArg(ctx)
    else:
        await func.invalidArg(ctx)

bot.run(DISCORD_API_TOKEN)
