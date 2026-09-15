import os
import asyncio
import discord

GUILD_ID = 1396485156197634067
DELAY = 0.5

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Бот запущен: {client.user}")

    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("Сервер не найден.")
        await client.close()
        return

    print(f"Сервер: {guild.name}")
    print(f"Участников: {len(guild.members)}")

    bot_member = guild.me

    for member in list(guild.members):

        # Владелец сервера
        if member == guild.owner:
            print(f"Пропуск владельца: {member}")
            continue

        # Discord не позволяет банить участников
        # с ролью выше или равной роли бота
        if member.top_role >= bot_member.top_role:
            print(f"Пропуск из-за иерархии: {member}")
            continue

        try:
            await member.ban(
                reason="Server cleanup",
                delete_message_seconds=0
            )

            print(f"Забанен: {member} | ID: {member.id}")

        except Exception as e:
            print(f"Не удалось забанить {member}: {e}")

        await asyncio.sleep(DELAY)

    print("Готово.")
    await client.close()


if not TOKEN:
    print("Ошибка: DISCORD_TOKEN не найден.")
else:
    client.run(TOKEN)
