import discord
import yaml
from discord.ext import commands

# settings and global variables
filename = None
with open('channel.yml', 'rt', encoding='utf8') as yml:
    channel = yaml.load(yml, Loader=yaml.FullLoader)

with open('userblock.yml', 'rt', encoding='utf8') as yml:
    userblock = yaml.load(yml, Loader=yaml.FullLoader)
Client = discord.Client()
client = commands.Bot(command_prefix = "!")
client.remove_command('help')