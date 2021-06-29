# Использовать этот файл для тестирование некоторых частей бота.

import discord
import random
from discord.ext import commands
from config import FuncA

# Ниже можно работать (То что удалять нельзя будет обозначено знаком "*").
PREFIX = FuncA['PREFIX']  # *
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())  # *


@client.event  # *
async def on_ready():  # *
    print('bot is waiting')  # *


# Здесь писать тестовую хуйню разную


# Ниже редактировать нельзя.
client.run(FuncA['TOKEN'])
