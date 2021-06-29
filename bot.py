import random
# import sqlite3
import discord
from discord_components import DiscordComponents, Button
from discord.ext import commands, tasks
from config import FuncA, color, status, kernel32
import termcolor

# Убрать решетки когда нужно будет работать над теми частями где нужны эти модули которые в "решетке"

PREFIX = FuncA['PREFIX']
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
client.remove_command('help')


# connection = sqlite3.connect('info.db')
# cursor = connection.cursor()


@client.event
async def on_ready():
    change_status.start()
    DiscordComponents(client)
    termcolor.cprint("Бот запущен успешно", 'green', attrs=['bold'])
    # Мне так в падлу импортировать если честно, но я импортирую, когда нибудь, честно.


#    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
#        name TEXT,
#        id INT,
#        cash INT,
#        lvl INT
#        )""")
#    # Создает "экономическую" базу данных
#    connection.commit()
#    # Подтверждает изменения в базе данных
#
#    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
#    role_id INT,
#    id INT,
#    cost BIGINT
#    )""")
#    # Создает магазин для экономической части.
#    connection.commit()
#    # Подтверждает изменения в базе данных
#
#    for guild in client.guilds:
#        for member in guild.members:
#            if cursor.execute(
#                    f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
#                # Проверка пользователя на существования в базе.
#                cursor.execute(
#                    f"INSERT INTO users VALUES ('{member}', '{member.id}', '0', '0')")
#                # Записывает пользователя в базу данных.
#                connection.commit()
#                # Подтверждает изменения в базе данных.
#    print('Data base connected')


# @client.event
# async def on_member_join(member):
#    """Если новый пользователь заходит на сервер он будет записан в базу данных."""
#    cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
#    data = cursor.fetchone()
#
#    if data is None:
#        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (member, member.id, 0, 0))
#        connection.commit()  # Подтверждает изменения в базе данных.
#    else:
#        pass


# @client.command(aliases=['Balance', 'bal', 'balance', 'Bal', 'Cash', 'cash'])
# async def __balance(ctx, member: discord.Member = None):
#    """Команда для того чтобы узнать свой/чужой баланс."""
#    if member is None:
#        await ctx.send(f"""**{ctx.author}** balance is **{
#        cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#        }**""")
#        # Показывает баланс пользователя.
#    elif cursor.execute(f"IN users NOT EXISTS member"):
#        await ctx.send(f"""**{ctx.author}** this user is not exists""")
#    else:
#        await ctx.send(f"""**{ctx.author}** balance is **{
#        cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
#        }**""")
#        # Показывает чужой баланс.


# @client.command(aliases=['Award', 'aw', 'award', 'Aw'])
# @commands.has_permissions(manage_messages=True)
# async def __award(ctx, member=None, amount: int = None):
#     """Команда для администраторов. Выдает определенное кол-во денег."""
#     if member is None:
#         # Проверка. Если пользователь не выбран говорит об этом в чате.
#         # Проверка. Если не выбрано кол-во денег.
#          embed = discord.Embed(
#             description=f"**{ctx.author}** please select user",
#             color=random.choice(color)
#        )
#        await ctx.send(embed=embed)
#    else:
#        if amount is None:
#            # Проверка. Если не выбрано кол-во денег.
#            embed = discord.Embed(
#                description=f"**{ctx.author}** please select amount",
#                color=random.choice(color)
#            )
#            await ctx.send(embed=embed)
#        elif amount < 1:
#            # Проверка. Если выбрано отрицательное кол-во денег
#            embed = discord.Embed(
#                description=f"**{ctx.author}** please select amount more than 1",
#                color=random.choice(color)
#            )
#            await ctx.send(embed=embed)
#        else:
#            # Передает определенное кол-во денег пользователю.
#            cursor.execute("UPDATE users SET cash = cash + {}".format(amount, member.id))
#            connection.commit()
#            # Подтверждает изменения в базе данных.
#            embed = discord.Embed(
#                description=f"**{ctx.author}** awarded **{member}**",
#                color=random.choice(color)
#            )
#            await ctx.send(embed=embed)


# @client.command(aliases=['add_role'])
# @commands.has_permissions(manage_messages=True)
# async def __add_role(ctx, role: discord.Role = None, cost: int = None):
#     """Команда для администрации. Добавляет роль для покупки."""
#     cursor.execute("INSERT INTO shop VALUES (?, ?, ?)".format(role.id, ctx.guild.id, cost))
#     connection.commit()
#     # Подтверждает изменения в базе данных.
#     await ctx.send('Done')


# @client.command(aliases=['buy', 'Buy'])
# async def __buy(ctx, role: discord.Role = None):
#     """Покупка ролей и др."""
#    if role is None:
#        # Проверка. Если роль не выбрана то будет сообщение.
#        await ctx.send(f"**{ctx.author}** select role to buy")
#    else:
#        if role in ctx.author.roles:
#            # Проверка. Если роль уже куплена.
#            await ctx.send(f"**{ctx.author}** you already have this role")
#        elif cursor.execute(
#                # Проверка. Если недостаточно валюты для покупки.
#                "SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
#                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
#            await ctx.send(f"**{ctx.author}** you have not enough money to buy that role")
#        else:
#            # Покупка. Если все пройдет успешно роль будет куплена.
#            await ctx.author.add_roles(role)
#            cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(
#                cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
#                ctx.author.id))
#            connection.commit()
#            # Подтверждает изменения в базе данных.
#
#            await ctx.send(f'**{ctx.author}** successfully bought role')


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


# @client.command(aliases=['Leadbd', 'leadbd', 'Leaderboard', 'leaderboard'])
# async def __leaderboard(ctx):
#     """Таблица лидеров."""
#     embed = discord.Embed(title='Top 10 economy', color=random.choice(color))
#     counter = 0
#     for row in cursor.execute("SELECT name, cash FROM users ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
#         counter += 1
#         embed.add_field(
#             name=f'# {counter} | `{row[0]}`',
#             value=f'Balance: {row[1]}',
#         )
#     await ctx.send(embed=embed)


# ===========================================
# ============ Основные комманды ============
# ===========================================


@client.event
async def on_member_join(member):
    """При присоединении участника выдает ему роли"""
    role1 = discord.utils.get(member.guild.roles, name='role1')
    # role1 = discord.utils.get(member.guild.role, name='Никто')
    # role2 = discord.utils.get(member.guild.role, name='—————————————————')
    # role3 = discord.utils.get(member.guild.role, name='————————————————')
    await member.add_roles(role1  # , role2, role3
                           # При включении бота в сервер нужно подставить эти значения.
                           )


@client.event
async def on_raw_reaction_add(payload):
    """При добавлении реакции на сообщение выдает роль."""
    message_id = payload.message_id
    if message_id == 813471933571924030:
        # Поменять ID сообщения при встраивании в сервер
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id is guild_id, client.guilds)

        if payload.emoji.name == 'male_sign':
            role = discord.utils.get(guild.roles, name='role1')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        # Тут тоже все поменять нужно при встраивании
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
    """При удалении реакции на сообщение забирает роль."""
    message_id = payload.message_id
    if message_id == 813392723833913355:
        # И тут...
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id is guild_id, client.guilds)

        if payload.emoji.name == 'male_sign':
            role = discord.utils.get(guild.roles, name='role1')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        # И тут....
        if role is not None:
            member = discord.utils.find(lambda m: m.id is payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("done")
            else:
                print("Member not found")
        else:
            print("Role not found")


@client.command(aliases=['Help', 'help', 'HELP'])
async def hlp(ctx):
    """Сообщение-помощь для пользователей с командами от бота."""
    embed = discord.Embed(
        title=f'**Префикс бота: "{PREFIX}"**',
        description='*Это бот который был построен на подобии mee6 и должен его заменить.*',
        colour=random.choice(color)
    )
    embed.set_footer(text='Иконку сделал ElectricStepa, бота сделал T0CHKA')
    embed.set_thumbnail(url='https://i.ibb.co/NZV1dMP/bot-icon.png')
    embed.add_field(name='**8Ball**', value='*Классический 8Ball. Отправляет случайный ответ на ваш вопрос.*',
                    inline=True)
    embed.add_field(name='**Clear <кол-во>**', value='*Убирает сообщения в чате. Только для модераторов и выше.*',
                    inline=True)
    embed.add_field(name='**Ping**', value='*ПОНГ! Проверяет пинг бота.*', inline=True)
    embed.add_field(name='**Rank**', value='*Показывает опыт и деньги участника.* ***(В РАЗРАБОТКЕ)***', inline=True)
    embed.add_field(name='**Help**', value='*Показывает это сообщение.*', inline=True)
    embed.add_field(name='**Links**', value='*Показывает наши ссылки.*', inline=True)
    embed.add_field(name='**Meme**', value='*Высылает рандомный мем.*', inline=True)
    embed.add_field(name='**RandNum <макс. число>**', value='*Выбирает случайное число*', inline=True)
    await ctx.send(
        #       components=[
        #       Button(style=2, label='Ping', custom_id='pong'),
        #       Button(style=2, label='Rank', custom_id='ronk'),
        #       Button(style=2, label='Links', custom_id='lonks')
        #   ],
        # Эти строки делают кнопки (они рабочие)
        embed=embed)


#
#    interaction = await client.wait_for("button_click", check=lambda r: r.component.label.startswith("WOW"))
#    await interaction.respond(content="Button clicked!")
#    interaction = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("WOW"))
#    await interaction.respond(content="Button clicked!")
#    interaction = await client.wait_for("button_click", check=lambda c: c.component.label.startswith("WOW"))
#    await interaction.respond(content="Button clicked!")

# В реализации это должно было вызывать команду при нажатии кнопки
# Но из-за лямбд нихрена не понятно и тут соотв-но не работает как надо

@client.command(aliases=['LINKS', 'Links'])
async def links(ctx):
    """Выводит сообщение пользователю с ссылками на контактные данные разработчика и его группы."""
    embed = discord.Embed(
        title='Вот наши ссылки:',
        colour=random.choice(color)
    )
    await ctx.send(components=[
        Button(style=5, label="Twitch", url="https://twitter.com/t0chka2020", emoji=':Twitch:'),
        Button(style=5, label="Twitter", url="https://twitter.com/t0chka2020", emoji=':Twitter:'),
        Button(style=5, label="Steam", url="https://steamcommunity.com/profiles/76561198330419173/", emoji=':Steam:')
    ],
        embed=embed,
    )


@tasks.loop(seconds=15)
async def change_status():
    """Меняет статус бота."""
    await client.change_presence(activity=discord.Game(next(status)))


@client.command(aliases=['Ping', 'PING'])
async def ping(ctx):
    """Команда для того чтобы узнать пинг бота."""
    embed = discord.Embed(
        description=f"Pong! Пинг бота {round(client.latency * 1000)}мс",
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@client.command(aliases=["8ball", '8BALL'])
async def _8ball(ctx):
    """Команда для развлечений, выводит случайный ответ типа Да/Нет."""
    responses = ["Да",
                 "Наверное",
                 "Нет",
                 "__Определенно__ нет",
                 "Первое",
                 "Второе",
                 "Ничего из этого",
                 "Спроси снова",
                 "Неа",
                 "__Определенно__ да"]
    embed = discord.Embed(
        description=f'{random.choice(responses)}',
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@client.command(aliases=['Mute', 'mute', 'MUTE'])
@commands.has_permissions(manage_messages=True)
async def user_mute(ctx, member: discord.Member):
    """Команда для того чтобы заткнуть пользователя."""
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')

    if member.roles is mute_role:
        embed = discord.Embed(
            description='Этот пользователь уже в муте.',
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        await member.add_roles(mute_role)
        embed = discord.Embed(
            description=f'{member} теперь молчит.',
            color=random.choice(color)
        )
    await ctx.send(embed=embed)


@client.command(aliases=['Clear', 'CLEAR'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    """Команда для того чтобы удалить определенное кол-во сообщений."""
    if amount is None:
        embed = discord.Embed(
            description=f'{ctx.author.mention} пожалуйста укажите кол-во.',
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    elif amount < 1:
        embed = discord.Embed(
            description=f'{ctx.author.mention} пожалуйста укажите значение больше нуля числах.',
            color=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount + 1)


@client.command(aliases=['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    """Команда для того чтобы разрешить пользователю разговаривать."""
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.remove_roles(mute_role)
    embed = discord.Embed(
        description=f'{member} теперь без заклеенного рта.',
        color=random.choice(color)
    )
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    """При ошибке вместо записывание ошибки в строку выводит сообщение о том что пользователь ошибся."""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            description=f'{ctx.author.mention} этой команды не существует.',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description=f'{ctx.author.mention} у тебя недостаточно возможностей для использования этой команды.',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)
#    elif isinstance(error, commands.MissingRequiredArgument):
#        embed = discord.Embed(
#            title=f'{ctx.author.mention} в команде отсутствуют нужные аргументы.',
#            colour=random.choice(color)
#        )
#        await ctx.send(embed=embed)
#        Здесь есть какие-то проблемы, так что пока что эта команда на паузе так сказать.
    else:
        pass

    # elif isinstance(error, commands.)
    #   embed = discord.Embed(
    #       description=f'{ctx.author.mention}',
    #       colour=random.choice(color)
    #   )
    #   await ctx.send(embed=embed)
    # В случае чего - дополнить


@client.command(aliases=['Meme', 'MEME'])
async def meme(ctx):
    """Высылает картинку в канал где была использована команда"""
    a = random.randrange(0, 11, 1)
    a
    if a == 1:
        await ctx.send(r'https://i.ibb.co/TWVvcQ7/pg5-QFpc-R7c.jpg')
    elif a == 2:
        await ctx.send(r'https://i.ibb.co/CtByYks/VSCsusk-g-Lo.jpg')
    elif a == 3:
        await ctx.send(r'https://i.ibb.co/HtfbvwH/Y7-PNA3a-LK7c.jpg')
    elif a == 4:
        await ctx.send(r'https://i.ibb.co/n8mRdn1/Z6-Uynt38q58.jpg')
    elif a == 5:
        await ctx.send(r'https://i.ibb.co/27h87Gf/6-WV35t20-Qi-Q.jpg')
    elif a == 6:
        await ctx.send(r'https://i.ibb.co/RjCFZm2/G-ENTr-Abpn4.jpg')
    elif a == 7:
        await ctx.send(r'https://i.ibb.co/qntHF8x/h-XJh-R5-EH-z0.jpg')
    elif a == 8:
        await ctx.send(r'https://i.ibb.co/QFbR1GL/p4-WNO4915i-A.jpg')
    # Наверное, самый тупой, но и одновременно самый простой и работающий способ (на некоторое время так постоит)
    # На данный момент я просто не знаю как сделать парсинг чтобы брать ссылки на изображения
    # Да еще и так чтобы это работало, ну эт вщ пздц.


@client.command(aliases=['RN', 'rn', 'RANDNUM', 'randnum'])
async def RandNum(ctx, amount1: int = None):
    """Выводит случайное число от 0 до того значения которое указал пользователь"""
    if amount1 < 1:
        embed = discord.Embed(
            description=f'{ctx.author.mention} Пожалуйста укажите число больше нуля и в целых числах.',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)
    elif amount1 is None:
        embed = discord.Embed(
            description=f'{ctx.author.mention} Пожалуйста укажите число.',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description=f'{ctx.author.mention} {random.randrange(0, amount1, 1)}',
            colour=random.choice(color)
        )
        await ctx.send(embed=embed)


# @client.command(aliases=[])
# async def (ctx)
#   Здесь написать новую команду.
#   await ctx.send(embed=embed)


client.run(FuncA['TOKEN'])
