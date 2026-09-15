import os
import asyncio
import discord

# =========================================================
# НАСТРОЙКИ
# =========================================================

GUILD_ID = 1127290770026676325
NEW_CHANNEL_NAME = "new-channel"

GIF_URL = "https://i.pinimg.com/originals/16/7f/75/167f75d8b3a387e66896316ea084fec8.gif"

DELAY = 0.5


# =========================================================
# DISCORD
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN не найден!")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# =========================================================
# БАН ВСЕХ
# =========================================================

async def ban_everyone(guild):

    print("========== БАН УЧАСТНИКОВ ==========")

    members = list(guild.members)

    print(f"Найдено участников: {len(members)}")

    for member in members:

        # Владельца сервера забанить нельзя
        if member.id == guild.owner_id:
            print(f"[SKIP OWNER] {member}")
            continue

        # Discord запрещает банить участника,
        # если его высшая роль выше/равна роли бота
        if member.top_role >= guild.me.top_role:
            print(f"[SKIP ROLE] {member}")
            continue

        try:
            await member.ban(
                reason="Automated server cleanup",
                delete_message_seconds=0
            )

            print(
                f"[BAN] {member} | ID: {member.id}"
            )

            await asyncio.sleep(DELAY)

        except discord.Forbidden:
            print(f"[FORBIDDEN] {member}")

        except discord.HTTPException as e:
            print(f"[HTTP ERROR] {member}: {e}")

        except Exception as e:
            print(f"[ERROR] {member}: {e}")

    print("====================================")
    print()


# =========================================================
# УДАЛЕНИЕ ВСЕХ РОЛЕЙ
# =========================================================

async def delete_all_roles(guild):

    print("========== УДАЛЕНИЕ РОЛЕЙ ==========")

    roles = list(guild.roles)

    print(f"Всего ролей: {len(roles)}")

    for role in roles:

        # @everyone удалить невозможно
        if role.is_default():
            print("[SKIP] @everyone")
            continue

        # Роль бота и роли выше него удалить нельзя
        if role >= guild.me.top_role:
            print(
                f"[SKIP] {role.name} "
                "(роль выше/равна боту)"
            )
            continue

        try:

            name = role.name

            await role.delete(
                reason="Automated server cleanup"
            )

            print(f"[DELETE ROLE] {name}")

            await asyncio.sleep(DELAY)

        except discord.Forbidden:
            print(f"[FORBIDDEN] {role.name}")

        except discord.HTTPException as e:
            print(f"[HTTP ERROR] {role.name}: {e}")

        except Exception as e:
            print(f"[ERROR] {role.name}: {e}")

    print("====================================")
    print()


# =========================================================
# УДАЛЕНИЕ ВСЕХ КАНАЛОВ
# =========================================================

async def delete_all_channels(guild):

    print("========== УДАЛЕНИЕ КАНАЛОВ ==========")

    channels = list(guild.channels)

    print(f"Всего каналов: {len(channels)}")

    for channel in channels:

        try:

            name = channel.name

            await channel.delete(
                reason="Automated server cleanup"
            )

            print(f"[DELETE CHANNEL] #{name}")

            await asyncio.sleep(DELAY)

        except discord.Forbidden:
            print(f"[FORBIDDEN] #{channel.name}")

        except discord.HTTPException as e:
            print(f"[HTTP ERROR] #{channel.name}: {e}")

        except Exception as e:
            print(f"[ERROR] #{channel.name}: {e}")

    print("=======================================")
    print()


# =========================================================
# СОЗДАНИЕ НОВОГО КАНАЛА
# =========================================================

async def create_channel(guild):

    print("Создаю новый канал...")

    try:

        channel = await guild.create_text_channel(
            NEW_CHANNEL_NAME,
            reason="Automated server setup"
        )

        print(f"[CREATED] #{channel.name}")

        return channel

    except discord.Forbidden:
        print("Нет права Manage Channels.")

    except discord.HTTPException as e:
        print(f"[HTTP ERROR] {e}")

    return None


# =========================================================
# ОТПРАВКА GIF
# =========================================================

async def send_gif(channel):

    print("Отправляю GIF...")

    try:

        await channel.send(GIF_URL)

        print("[GIF] GIF отправлена.")

    except discord.HTTPException as e:

        print(f"[GIF ERROR] {e}")


# =========================================================
# ЗАПУСК
# =========================================================

@client.event
async def on_ready():

    print()
    print("====================================")
    print(f"Бот запущен: {client.user}")
    print("====================================")

    guild = client.get_guild(GUILD_ID)

    if guild is None:

        print("Сервер не найден.")
        await client.close()
        return

    print(f"Сервер: {guild.name}")
    print(f"Участников: {guild.member_count}")
    print()

    permissions = guild.me.guild_permissions

    print("============= ПРАВА =============")
    print(f"Administrator:    {permissions.administrator}")
    print(f"Ban Members:      {permissions.ban_members}")
    print(f"Manage Roles:     {permissions.manage_roles}")
    print(f"Manage Channels:  {permissions.manage_channels}")
    print("=================================")
    print()

    # =====================================================
    # 1. БАНИМ ВСЕХ
    # =====================================================

    await ban_everyone(guild)

    # =====================================================
    # 2. УДАЛЯЕМ ВСЕ РОЛИ
    # =====================================================

    await delete_all_roles(guild)

    # =====================================================
    # 3. УДАЛЯЕМ ВСЕ КАНАЛЫ
    # =====================================================

    await delete_all_channels(guild)

    # =====================================================
    # 4. СОЗДАЁМ НОВЫЙ КАНАЛ
    # =====================================================

    channel = await create_channel(guild)

    if channel is not None:

        # =================================================
        # 5. ОТПРАВЛЯЕМ GIF
        # =================================================

        await send_gif(channel)

    print()
    print("====================================")
    print("ОПЕРАЦИЯ ЗАВЕРШЕНА")
    print("====================================")

    await client.close()


# =========================================================
# START
# =========================================================

client.run(TOKEN)
