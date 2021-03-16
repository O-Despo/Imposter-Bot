import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
#adding to git repo for ex
load_dotenv()
TOKEN = str(os.getenv('TOKEN'))

bot = discord.ext.commands.Bot(command_prefix = "IB-");
guilds_dict = {}

class game:
    def __init__(self, game_name, code, owner, players:list, game_data_list:list):
        '''Verify input info then appends necessary info into a list called game_data'''
        #all the data is stored in a dict for later call
        game_data = make_dict_from_import_list(game_data_list)
        game_data['code'] = code.upper()
        game_data['name'] = game_name
        game_data['players'] = players
        game_data['owner'] = owner
        game_data['time'] = 'null'
        self.game_data = game_data
        print(self.game_data)

    def get_code(self):
        '''gets code'''
        return(self.game_data['code'])

    def get_owner(self):
        '''gets code'''
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

    def verify_player_change(self, author, player_list, ):
        '''used in add and remove to verify that the input list is not
        empty, the owner is not removed and the owner is executing the command'''

        if self.verify_owner(author) == False:
            response = f'Only the game owner can remove players'
            return False, 1
        elif self.game_data['owner'] in player_list:
            response = f'You have attempted to remove the owner form the game\
            this is not possible'
            return False, 2
        elif not player_list:
            response = f'The player list is empty please add players after the\
                 game name'
            return False, 3
        else:
            return True, 0
    
    def set_code(self, new_code):
        '''set new game code only unsalable by game Owner'''
        self.game_data['code'] = new_code

        response = f"{self.game_data['code']} code is now {new_code}"
        return

    def verify_owner(self, name):
        '''used to verify owner'''
        if name == self.game_data['owner']:
            return True
        else:
            return False

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
    
    def remove_players(self, author, players):
        '''Removes players only for owner'''
        #This statement server to verify that the action can be taken
        #ensure owners is making the action and not removing themselves 
        error_response_dict = {
            1: 'Only the game owner can remove players',
            2: 'You have attempted to remove the owner form the game not possible',
            3: 'The player list is empty please add players after the game name'
        }
        
        is_verified, error_case = self.verify_player_change(author, players)

        if is_verified != True:
            response = error_response_dict[error_case]
            return response

        unmoved_players = []
        current_players = self.game_data['players']
        all_removed = True

        #Checks that the players that are being removed are in the game
        players = list(players)
        for player in players:
            if player in current_players:
                current_players.remove(player)
            else:
                unmoved_players.append(player)
                all_removed = False

        if all_removed != False:
            response = f"Those players have been removed"
        else:
            response = f"Most requested players were removed \
            {unmoved_players} not in the game"
        
        return response

    def add_players(self, author, players):
        '''adds players only for owner'''

        #error check 
        error_response_dict = {1: 'Only the game owner can remove players',
        2: 'You have attempted to remove the owner form the game this is not possible',
        3: 'The player list is empty please add players after the game name'}

        is_verified, error_case = self.verify_player_change(author, players)

        if is_verified != True:
            response = error_response_dict[error_case]
            return response
        
        #adds players 
        current_palyers = self.game_data['players']
        players = list(players)

        if len(current_palyers) > 10 or len(current_palyers) + len(players) > 10:
            response = 'To many players a game can not have more than 10'
            return(response)

        for player in players:
             if player in current_palyers:
                response = f"This player is already in the game"

                return(response)

        else:
            self.game_data['players'] = list(players) + current_palyers

            response = f"successfully added to {self.game_data['name']}"
        
            return(response)
    
    def rsvp(self, author_list):
        players = self.game_data['players']
        game = self.game_data['name']
        author = author_list[0]

        if author in players:
            response = 'you are already in the game'
            return response
        elif len(players) >= 10:
            response = 'there are already 10 players in the game'
            return response

        new_players = players + author
        self.game_data['players'] = new_players

        response = f'You have been added to {game}'
        
        return response
    
    def unrsvp(self, author_list):
        players = self.game_data['players']
        game = self.game_data['name']
        game_owner = self.game_data['owner']
        author = author_list[0]

        if not author in players:
            response = f'you were never in {game}'
            return response
        elif author == game_owner:
            response = f'you are the game owner and cannot be removed'
            return response

        new_players = players.remove(author)
        self.game_data['players'] = new_players

        response = f'You have been added to {game}'
        
        return response
    
    def set_time(self, time, author):
        '''
        sets time for game only usable by owner
        '''
        if self.verify_owner(author):
            old_time = self.game_data['time']
            game_name = self.game_data['name']
            self.game_data['time'] = time

            response = f'Changed {game_name} time form {old_time} to {time}'

            return response

        else:
            response = 'You are not onwer and cannot use that command'

            return response
    
    def time(self, author):
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

@bot.command(name='make-game', help='creates a game make-game {gamename} {code}')
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

@bot.command(name='set-code', help='sets code for the specified game')
async def code(ctx, game_name:str):
    game_object = guilds_dict[ctx.guild.name][game_name]

    code = game_object.get_code()
    await ctx.send(code)

@bot.command(name='players', help='shows game players')
async def code(ctx, game_name:str):
    game_object = guilds_dict[ctx.guild.name][game_name]

    response = game_object.players()
    await ctx.send(response)

@bot.command(name='game-info', help='shows all info for the specified game')
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

    return_message = game_object.rsvp([ctx.author.name])

    await ctx.send(return_message)

@bot.command(name='UNRSVP', help='Remove yourself form game')
async def unrsvp(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]
    return_message = game_object.unrsvp([ctx.author.name])

    await ctx.send(return_message)

@bot.command(name='add', help='add {game-Name} puts players down to play in a game')
async def rsvp(ctx, game_name, *players_to_add):
    game_object = guilds_dict[ctx.guild.name][game_name]
    return_message = game_object.add_players(ctx.author.name, players_to_add)

    await ctx.send(return_message)

@bot.command(name='remove', help='remove {game-Name} removes players in a game')
async def remove(ctx, game_name, *players_to_remove):
    game_object = guilds_dict[ctx.guild.name][game_name]
    author = ctx.author 

    return_message = game_object.remove_players(author, players_to_remove)

    await ctx.send(return_message)

@bot.command(name='owner', help='Owner of game')
async def owner(ctx, game_name):
    game_object = guilds_dict[ctx.guild.name][game_name]
    response = game_object.get_owner()

    await ctx.send(response)

@bot.command(name='set-time', help='sets the time of a game')
async def owner(ctx, game_name, time):
    game_object = guilds_dict[ctx.guild.name][game_name]
    response = game_object.set_time(time)

    await ctx.send(response)

@bot.command(name='time', help='shows game time')
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