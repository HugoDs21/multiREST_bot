import os
import requests
import functions as func
from discord.ext import commands
from datetime import date, timedelta, datetime

PREFIX = os.getenv('PREFIX') or "!"
DISCORD_API_TOKEN = os.getenv('DISCORD_API_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)

restaurants = {"fcup": 0, "feup": 2}

actions = {"help": func.getHelp, 
           "ajuda": func.getHelp,
           "h": func.getHelp,
           "hoje": func.getToday,
           "hj": func.getToday,
           "amanha": func.getTomorrow,
           "am": func.getTomorrow,
           "semana": func.getWeek,
           "sem": func.getWeek,
           }

@bot.event # on_ready
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def multirest(ctx, *args):
    instId = restaurants.get("fcup") #Default
    instName = "fcup"

    if len(args) == 0:
        await ctx.send(func.invalidArg())   

    possible_args = list(actions.keys()) + list(restaurants.keys())

    #get common elements between args and possible_args
    common_args = [x for x in args if x in possible_args]
    
    if len(common_args) == 1:
        if common_args[0] in actions:
            await ctx.send(actions[common_args[0]](instId, instName))
        else:
            await ctx.send(func.invalidArg())
    elif len(common_args) == 2:
        if "feup" in common_args:
            instId = restaurants.get("feup")
            instName = "feup"
        for x in common_args:
            if x in actions:
                await ctx.send(actions[x](instId, instName))
    else:
        pass
        
@bot.command()
async def mr(ctx, *args):
    await multirest(ctx, *args)        
        
bot.run(DISCORD_API_TOKEN)
