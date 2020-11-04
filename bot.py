import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))

bot = discord.ext.commands.Bot(command_prefix = "IB-");
guilds_dict = {}

class game:
    def __init__(self, game_name, code, players:list, game_data_list:list):
        '''
        Makes a game object with game_name and code required 
        any extra varbibles are imported as a list
        players must be passed as list
        the list is is in key value pairs but not a dict 
        '''
        game_data = make_dict_from_import_list(game_data_list)
        game_data['code'] = code
        game_data['name'] = game_name
        game_data['players'] = players
        self.game_data = game_data
        print(self.game_data)

    def get_code(self):
        response =  f'{self.game_name}: {self.code}'
        return(self.game_data['code'])

    def get_info(self):
        '''
        Loops through the all the data available 
        about a given game and returns a string response 
        '''
        response = 'All the available data is'

        for key, value in self.game_data.items():
            response = response + f'\n {key}: {value}'

        return response

    def rsvp(self, *players):
        '''
        takes a players name and apeends it to the list 
        of players that are going to play
        '''
        current_palyers = self.game_data['players']
        self.game_data['players'] = list(players) + current_palyers

        response = f"successfully added {players} to {self.game_data['name']}"
        
        return(response)

def make_dict_from_import_list(import_tuple):
    '''
    This is used for game innit to make the list into a dict
    '''
    return_dict = {}
    import_list = list(import_tuple)
    x = 0

    while x < len(import_list):
        key = import_list.pop(0)
        value = import_list.pop(0)

        return_dict[key] = value
        x += 1
    
    return return_dict

@bot.event
async def on_ready():
    guild_list = bot.guilds 
    guild_names = []

    for guild in guild_list:
        guild_names.append(guild.name)

    print(f'Connected: {bot.user} \n Guilds: {guild_names}')

@bot.command(name='make-game', help='creates a game \n \
    takes parameters name and code')
async def code(ctx, name:str, code:str, *data):
    #requires game name and code to init any other 
    # info is larter turned in dict
    player_list = [ctx.author.name]

    game_init = game(name, code, player_list, data)
    '''
    you need to
    if name in guilds_dict[ctx.guild.name]
    '''

    if ctx.guild.name in guilds_dict.keys():
        guilds_dict[ctx.guild.name].append({name: game_init})

    else:
        guilds_dict[ctx.guild.name] = []
        guilds_dict[ctx.guild.name].append({name: game_init})
    
    response = f'{ctx.author.name} created {name}'
    print(guilds_dict)
    await ctx.send(response)

        
@bot.command(name='game-code', help='shows code for the specified game')
async def code(ctx, game_name:str):
    game_object = games[game_name]

    code = game_object.get_code()
    await ctx.send(code)


@bot.command(name='game-info', help='shows code for the current game')
async def game_info(ctx, game_name:str):
    game_object = guilds_dict[ctx.guild.name][game_name]

    info = game_object.get_info()
    await ctx.send(info)

@bot.command(name='all', help='shows all the active games on the server')
async def view_all(ctx):
    guild_games = guilds_dict[ctx.guild.name]

    response = f'Current Games:'
    for x in guild_games.keys():
        response += f'{x}\n'
    
    await ctx.send(response)

@bot.command(name='RSVP', help='RSVP {game-Name} puts you down to play in a game')
async def rsvp(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]

    return_message = game_object.rsvp(ctx.author.name)

    await ctx.send(return_message)

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

'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: your command is incomplete")
    else:
        await ctx.send(error)
'''
bot.run(TOKEN)