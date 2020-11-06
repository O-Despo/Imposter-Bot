import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))

bot = discord.ext.commands.Bot(command_prefix = "-");
guilds_dict = {}

class game:
    def __init__(self, game_name, code, owner, players:list, game_data_list:list):
        '''
        Makes a game object with game_name and code required 
        any extra varbibles are imported as a list
        players must be passed as list
        the list is is in key value pairs but not a dict 
        '''
        game_data = make_dict_from_import_list(game_data_list)
        game_data['code'] = code.upper()
        game_data['name'] = game_name
        game_data['players'] = players
        game_data['owner'] = owner
        game_data['time'] = 'null'
        self.game_data = game_data
        print(self.game_data)

    def get_code(self):
        return(self.game_data['code'])

    def get_owner(self):
        return(self.game_data['owner'])

    def get_info(self):
        '''
        Loops through the all the data available 
        about a given game and returns a string response 
        '''
        response = 'All the available data is'

        for key, value in self.game_data.items():
            response = response + f'\n {key}: {value}'

        return response

    def players(self):
        '''
        returns a response of all the players in the game
        '''
        player_list = self.game_data['players']
        game_name = self.game_data['name']  
        response = f'The players in {game_name}'

        for player in player_list:
            response = response + f'\n{player}'

        return response
    
    def remove_players(self, input_players):

        unmoved_players = []
        current_players = self.game_data['players']
        all_removed = True

        input_players = list(input_players)
        for player in input_players:
            if player in current_players:
                current_players.remove(player)
            else:
                unmoved_players.append(player)
                all_removed = False

        if all_removed != False:
            response = f"Those players have been removed"
        else:
            response = f"All requested players were remove \
                {all_removed} were not in the game"
        
        return response

    def add_players(self, players):
        '''
        takes a players name and apeends it to the list 
        of players that are going to play will not append if player is already on list
        '''
        current_palyers = self.game_data['players']
        players = list(players)
        for player in players:
             if player in current_palyers:
                response = f"This player is already ready for the game"

                return(response)

        else:
            self.game_data['players'] = list(players) + current_palyers

            response = f"successfully added {players} to {self.game_data['name']}"
        
            return(response)

    def set_time(self, time):
        '''
        sets time for game
        '''
        old_time = self.game_data['time']
        game_name = self.game_data['name']
        self.game_data['time'] = time

        response = f'Changed {game_name} time form {old_time} to {time}'

        return response
    
    def time(self):
        '''
        gets time for game
        '''
        time = self.game_data['time']
        game_name = self.game_data['name']

        response = f' {game_name} time : {time}'

        return response
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

def verify_code(code):
    '''
    verify the and format of the game code
    '''
    if 6 == len(code) and code.isalpha():
        return True
    else: 
        return False
    
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
    '''
    requires game name and code to init any other 
    info is larter turned in dict
    '''

    #Verifies code before going futher
    if verify_code(code) != True:
        response = 'Please enter the game code correctly'

    else:
        player_list = [ctx.author.name]
        owner = ctx.author.name
        game_init = game(name, code, owner, player_list, data)

        #checks if the game has already been declared as a dict if not it decares it
        if not ctx.guild.name in guilds_dict.keys():
            guilds_dict[ctx.guild.name] = {}

        guilds_dict[ctx.guild.name][name] = game_init
        
        response = f'{ctx.author.name} created {name}'
        print(guilds_dict)
    
    await ctx.send(response)
        
@bot.command(name='code', help='shows code for the specified game')
async def code(ctx, game_name:str):
    game_object = guilds_dict[ctx.guild.name][game_name]

    code = game_object.get_code()
    await ctx.send(code)

@bot.command(name='players', help='players')
async def code(ctx, game_name:str):
    game_object = guilds_dict[ctx.guild.name][game_name]

    response = game_object.players()
    await ctx.send(response)

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
        response += f'\n{x}'
    
    await ctx.send(response)

@bot.command(name='RSVP', help='RSVP {game-Name} puts you down to play in a game')
async def rsvp(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]

    return_message = game_object.add_players([ctx.author.name])

    await ctx.send(return_message)

@bot.command(name='UNRSVP', help='Remove yourself form game')
async def unrsvp(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]
    return_message = game_object.remove_players([ctx.author.name])

    await ctx.send(return_message)

@bot.command(name='add', help='RSVP {game-Name} puts you down to play in a game')
async def rsvp(ctx, game_name, *players_to_add):
    game_object = guilds_dict[ctx.guild.name][game_name]
    return_message = game_object.add_players(players_to_add)

    await ctx.send(return_message)

@bot.command(name='remove', help='Removes the players listed')
async def remove(ctx, game_name, *players_to_remove):
    game_object = guilds_dict[ctx.guild.name][game_name]

    return_message = game_object.remove_players(players_to_remove)

    await ctx.send(return_message)

@bot.command(name='owner', help='Owners of game')
async def owner(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]
    response = game_object.get_owner()

    await ctx.send(response)

@bot.command(name='set-time', help='Owners of game')
async def owner(ctx, game_name, time):
    game_object = guilds_dict[ctx.guild.name][game_name]
    response = game_object.set_time(time)

    await ctx.send(response)

@bot.command(name='time', help='Owners of game')
async def owner(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]
    response = game_object.time()

    await ctx.send(response)

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

'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: your command is incomplete")
        print(error)
    else:
        await ctx.send(error)
        print(error)
'''
bot.run(TOKEN)