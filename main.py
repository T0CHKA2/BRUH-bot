import random
import discord
import sqlite3
from itertools import cycle
from discord.ext import commands, tasks
from config import FuncA

client = commands.Bot(command_prefix=FuncA['PREFIX'], intents=discord.Intents.all())
client.remove_command('help')
status = cycle(['Use "!help" for help', "If you find bug, tell it to T0CHKA#2838 or Sepulturēsa#1141"])
connection = sqlite3.connect('info.db')
cursor = connection.cursor()
color = (0xFFFFFF, 0x00FFFF, 0x0080FF, 0xFF00FF, 0x0000FF, 0xFFFF00, 0xFF8000, 0xFF0000, 0x00FF00)


@client.event
async def on_ready():
    change_status.start()
    print('Bot online')

    cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
        name TEXT,
        id INT,
        cash INT,
        lvl INT
        )""")
    # Создает "экономическую" базу данных
    connection.commit()
    # Подтверждает изменения в базе данных

    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
    role_id INT,
    id INT,
    cost BIGINT
    )""")
    # Создает магазин для экономической части.
    connection.commit()
    # Подтверждает изменения в базе данных

    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(
                    f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                # Проверка пользователя на существования в базе.
                cursor.execute(
                    f"INSERT INTO users VALUES ('{member}', '{member.id}', '0', '0')")
                # Записывает пользователя в базу данных.
                connection.commit()
                # Подтверждает изменения в базе данных.
    print('Data base connected')


@client.event
async def on_member_join(member):
    """Если новый пользователь заходит на сервер он будет записан в базу данных."""
    cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (member, member.id, 0, 0))
        connection.commit()  # Подтверждает изменения в базе данных.
    else:
        pass


@client.command(aliases=['Balance', 'bal', 'balance', 'Bal', 'Cash', 'cash'])
async def __balance(ctx, member: discord.Member = None):
    """Команда для того чтобы узнать свой/чужой баланс."""
    if member is None:
        await ctx.send(f"""**{ctx.author}** balance is **{
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        }**""")
        # Показывает баланс пользователя.
    elif cursor.execute(f"IN users NOT EXISTS member"):
        await ctx.send(f"""**{ctx.author}** this user is not exists""")
    else:
        await ctx.send(f"""**{ctx.author}** balance is **{
        cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
        }**""")
        # Показывает чужой баланс.


@client.command(aliases=['Award', 'aw', 'award', 'Aw'])
@commands.has_permissions(manage_messages=True)
async def __award(ctx, member=None, amount: int = None):
    """Команда для администраторов. Выдает определенное кол-во денег."""
    if member is None:
        # Проверка. Если пользователь не выбран говорит об этом в чате.
        # Проверка. Если не выбрано кол-во денег.
        embed = discord.Embed(
            description=f"**{ctx.author}** please select user",
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        if amount is None:
            # Проверка. Если не выбрано кол-во денег.
            embed = discord.Embed(
                description=f"**{ctx.author}** please select amount",
                color=random.choice(color)
            )
            await ctx.send(embed=embed)
        elif amount < 1:
            # Проверка. Если выбрано отрицательное кол-во денег
            embed = discord.Embed(
                description=f"**{ctx.author}** please select amount more than 1",
                color=random.choice(color)
            )
            await ctx.send(embed=embed)
        else:
            # Передает определенное кол-во денег пользователю.
            cursor.execute("UPDATE users SET cash = cash + {}".format(amount, member.id))
            connection.commit()
            # Подтверждает изменения в базе данных.
            embed = discord.Embed(
                description=f"**{ctx.author}** awarded **{member}**",
                color=random.choice(color)
            )
            await ctx.send(embed=embed)


@client.command(aliases=['add_role'])
@commands.has_permissions(manage_messages=True)
async def __add_role(ctx, role: discord.Role = None, cost: int = None):
    """Команда для администрации. Добавляет роль для покупки."""
    cursor.execute("INSERT INTO shop VALUES (?, ?, ?)".format(role.id, ctx.guild.id, cost))
    connection.commit()
    # Подтверждает изменения в базе данных.
    await ctx.send('Done')


@client.command(aliases=['buy', 'Buy'])
async def __buy(ctx, role: discord.Role = None):
    """Покупка ролей и др."""
    if role is None:
        # Проверка. Если роль не выбрана то будет сообщение.
        await ctx.send(f"**{ctx.author}** select role to buy")
    else:
        if role in ctx.author.roles:
            # Проверка. Если роль уже куплена.
            await ctx.send(f"**{ctx.author}** you already have this role")
        elif cursor.execute(
                # Проверка. Если недостаточно валюты для покупки.
                "SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f"**{ctx.author}** you have not enough money to buy that role")
        else:
            # Покупка. Если все пройдет успешно роль будет куплена.
            await ctx.author.add_roles(role)
            cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(
                cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
                ctx.author.id))
            connection.commit()
            # Подтверждает изменения в базе данных.

            await ctx.send(f'**{ctx.author}** successfully bought role')


# @client.command(aliases=['pay', 'Pay'])
# async def __pay(ctx, amount: int = None, member=None):
# if member is None:  # Проверка. Если пользователь не выбран будет выслано сообщение.
# await ctx.send(f"**{ctx.author}** please select user"),
# else:
# if amount is None:  # Проверка. Если пользователь не выбран будет выслано сообщение.
# await ctx.send(f"**{ctx.author}** please select amount of money that you wanna give"),
# else:
# cursor.execute("UPDATE users SET cash".format(
# cursor.execute("SELECT").format()).fetchone())
# connection.commit()  # Подтверждает изменения в базе данных.


@client.command(aliases=['Leadbd', 'leadbd', 'Leaderboard', 'leaderboard'])
async def __leaderboard(ctx):
    """Таблица лидеров."""
    embed = discord.Embed(title='Top 10 economy', color=random.choice(color))
    counter = 0
    for row in cursor.execute("SELECT name, cash FROM users ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
        counter += 1
        embed.add_field(
            name=f'# {counter} | `{row[0]}`',
            value=f'Balance: {row[1]}',
        )
    await ctx.send(embed=embed)


# ============ Основные комманды ============

@client.event
async def on_member_join(member):
    role1 = discord.utils.get(member.guild.roles, id='812043212197593088')
    # role1 = discord.utils.get(member.guild.role, id='723878908050800712')
    # role2 = discord.utils.get(member.guild.role, id='723879044273405982')
    # role3 = discord.utils.get(member.guild.role, id='723879272040628264')
    await member.add_roles(role1)  # role2, role3


@client.event
async def on_raw_reaction_add(payload):
    """При выставлении реакции на сообщение выдает роль."""
    message_id = payload.message_id
    if message_id == 813471933571924030:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id is guild_id, client.guilds)

        if payload.emoji.name == 'male_sign':
            role = discord.utils.get(guild.roles, name='role1')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id is payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")


@client.event
async def on_raw_reaction_remove(payload):
    """При убирании реакции на сообщение забирает роль."""
    message_id = payload.message_id
    if message_id == 813392723833913355:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id is guild_id, client.guilds)

        if payload.emoji.name == 'male_sign':
            role = discord.utils.get(guild.roles, name='role1')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id is payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")


@client.command(aliases=['Help', 'help'])
async def hlp(ctx):
    """Сообщение-помощь для пользователей с командами от бота."""
    embed = discord.Embed(
        title='**Bot prefix is "!"**',
        description='*This should be a description, but its not here ;)*',
        colour=random.choice(color)
    )
    embed.set_footer(text='Bot icon by ElectricStepa, bot by T0CHKA and Sepulturēsa')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/728961778767101973/743436041410838548/bot_icon.png')
    embed.add_field(name='**8Ball**', value='*Just classic 8Ball. Sending random answer on your question*', inline=True)
    embed.add_field(name='**Clear <amount>**', value='*Moderator command. Clears messages in channel*', inline=True)
    embed.add_field(name='**Ping**', value='*PONG! Checking bot ping.*', inline=True)
    embed.add_field(name='**Rank**', value='*Shows your Lvl and Exp* ***(WORK IN PROGRESS)***', inline=True)
    embed.add_field(name='**Help**', value='*Shows this message*', inline=True)
    embed.add_field(name='**Links**', value='*Shows our links*', inline=True)
    await ctx.send(embed=embed)


@client.command()
async def links(ctx):
    embed = discord.Embed(
        title='Here ours links:',
        colour=random.choice(color)
    )
    embed.add_field(name='Twitter', value='', inline=True)
    embed.add_field(name='Steam', value='', inline=True)
    embed.add_field(name='Twitch', value='', inline=True)
    await ctx.send(embed=embed)


@tasks.loop(seconds=15)
async def change_status():
    """Меняет статус бота."""
    await client.change_presence(activity=discord.Game(next(status)))


@client.command(aliases=['Ping'])
async def ping(ctx):
    """Команда для того чтобы узнать пинг бота."""
    embed = discord.Embed(
        description=f"Pong! Bot ping {round(client.latency * 1000)}ms",
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@client.command(aliases=["8ball"])
async def _8ball(ctx):
    """Команда для развлечений, выводит случайный ответ типа Да/Нет."""
    responses = ["Yes",
                 "Maybe",
                 "No",
                 "__Definitely__ no",
                 "First",
                 "Second",
                 "Nothing of it",
                 "Ask again",
                 "Nope",
                 "__Definitely__ yes"]
    embed = discord.Embed(
        description=f'{random.choice(responses)}',
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@client.command(aliases=['Mute', 'mute'])
@commands.has_permissions(manage_messages=True)
async def user_mute(ctx, member: discord.Member):
    """Команда для того чтобы заткнуть пользователя."""
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')

    if member.roles is mute_role:
        embed = discord.Embed(
            desc='This user already muted.',
            clr=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        await member.add_roles(mute_role)
        embed = discord.Embed(
            description=f'{member} Muted.',
            color=random.choice(color)
        )
    await ctx.send(embed=embed)


@client.command(aliases=['Clear'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    """Команда для того чтобы удалить определенное кол-во сообщений."""
    if amount is None:
        embed = discord.Embed(
            description=f'{ctx.author.mention} please enter amount.',
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    elif amount < 1:
        embed = discord.Embed(
            description=f'{ctx.author.mention} please enter full amount.',
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount + 1)


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    """Команда для того чтобы разрешить пользователю разговаривать."""
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.remove_roles(mute_role)
    embed = discord.Embed(
        description=f'{member} Un-muted.',
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@clear.error
async def clear_error(error, ctx):
    """При ошибке пользователя вместо записывание ошибки в лог выводит сообщение о том что юзер бака."""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            description=f'{ctx.author.mention} this command is not exists.',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description=f'{ctx.author.mention} you have not enough permissions for this command.',
            colour=random.choice(color)

        )
        await ctx.send(embed=embed)

client.run(FuncA['TOKEN'])
