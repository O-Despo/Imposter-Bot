import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

TOKEN = ''

bot = discord.ext.commands.Bot(command_prefix = "IB-");
guilds_dict = {}

class game:
    def __init__(self, game_name, code, **game_data):
        self.game_name = game_name
        self.code = code
        game_data['code'] = code
        game_data['name'] = game_name
        self.game_data = game_data
        print(self.game_data)

    def get_code(self):
        response =  f'{self.game_name}: {self.code}'
        return(self.code)

    def get_info(self):
        response = f'Name:{self.game_name}\n \
            Code:{self.code}\n \
            Mode:{self.mode}\n \
            Map:{self.map}'

        return response

@bot.event
async def on_ready():
    guild_list = bot.guilds 
    guild_names = []

    for guild in guild_list:
        guild_names.append(guild.name)

    print(f'Connected: {bot.user} \n Guilds: {guild_names}')

@bot.command(name='make-game', help='creates a game \n \
    takes parameters name and code')
async def code(ctx, name:str, code:str):
    game_init = game(name, code)

    guilds_dict[ctx.guild.name] = {name: game_init}
    
    await ctx.send(guilds_dict)

@bot.command(name='whos-imposter', help='tells you who is imposter')
async def imposter(ctx):
    guild = ctx.guild
    members_list = []

    for member in guild.members:
        members_list.append(member.display_name)

    
    imposter = 'Imposter-Bot'

    while imposter == 'Imposter-Bot':
        imposter = random.choice(members_list)

    response_options = [
    f'{imposter} is sus', 
    f'Shhhhhh... the imposter is {imposter}',
    f'It is not {imposter}... unless',
    ]
    
    response = random.choice(response_options)
    await ctx.send(response)

    response = f'created game {name} with code {code}'
    await ctx.send(response)

@bot.command(name='game-code', help='shows code for the current game')
async def code(ctx, game_name:str):
    game_object = games[game_name]

    code = game_object.get_code()
    await ctx.send(code)

@bot.command(name='game-info', help='shows code for the current game')
async def game_info(ctx, game_name:str):
    game_object = games[game_name]

    info = game_object.get_info()
    await ctx.send(info)


@bot.command(name='guilds')
async def guilds(ctx):
    guild = (ctx.guild)

    await ctx.send(guild)
bot.run(TOKEN)
