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

    me = guild.me

    print(f"Сервер: {guild.name}")
    print(f"Роль бота: {me.top_role.name}")
    print(f"Всего участников: {len(guild.members)}")

    for member in list(guild.members):

        # Владелец сервера
        if member.id == guild.owner_id:
            print(f"[SKIP] Владелец: {member}")
            continue

        # Проверка иерархии Discord
        if member.top_role >= me.top_role:
            print(
                f"[SKIP] {member} — "
                f"роль '{member.top_role.name}' "
                f">= роли бота '{me.top_role.name}'"
            )
            continue

        try:
            await guild.ban(
                member,
                reason="Server cleanup",
                delete_message_seconds=0
            )

            print(f"[BAN] {member} | {member.id}")

        except discord.Forbidden:
            print(f"[FORBIDDEN] {member} — Discord отклонил бан")

        except discord.HTTPException as e:
            print(f"[HTTP ERROR] {member}: {e}")

        except Exception as e:
            print(f"[ERROR] {member}: {e}")

        await asyncio.sleep(DELAY)

    print("Готово.")
    await client.close()


if not TOKEN:
    print("DISCORD_TOKEN не найден!")
else:
    client.run(TOKEN)
