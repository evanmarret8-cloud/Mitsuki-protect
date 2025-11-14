import discord
from discord.ext import commands
from keep_alive import keep_alive
import asyncio
import os

keep_alive()

############################################################
#              INTENTS
############################################################

intents = discord.Intents.all()
bot_protect = commands.Bot(command_prefix="!", intents=intents)

############################################################
#              CONFIGURATION
############################################################

bad_words = ["ntm", "ntr", "bztmr", "tmrlpt", "fdp", "serv de mrd"]
warns = {}
ban_links = ["discord.gg/", "discord.com/invite"]

LOG_CHANNEL_ID = 1438450239483678793

async def send_log(message: str):
    channel = bot_protect.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

############################################################
#              EVENT : MESSAGE PROTECT
############################################################

@bot_protect.event
async def on_message(message):
    if message.author.bot:
        return

    # Les admins ne sont pas filtrés
    if message.author.guild_permissions.administrator:
        return await bot_protect.process_commands(message)

    msg = message.content.lower().split()

    # Détection insultes
    for bad_word in bad_words:
        if bad_word in msg:
            await message.delete()
            await warn_user(message.author, message.channel, f"Mot interdit : `{bad_word}`")
            return

    # Détection liens Discord
    for link in ban_links:
        if link in message.content.lower():
            await message.delete()
            await warn_user(message.author, message.channel, "Lien Discord interdit")
            return

    await bot_protect.process_commands(message)

############################################################
#              GESTION DES WARNS
############################################################

async def warn_user(user, channel, reason):
    warns[user.id] = warns.get(user.id, 0) + 1
    count = warns[user.id]

    await channel.send(f"⚠️ {user.mention} avertissement {count}/20 : {reason}")
    await send_log(f"[WARN] {user} → {reason} ({count})")

############################################################
#              COMMANDES ADMIN
############################################################

@bot_protect.command()
@commands.has_permissions(administrator=True)
async def warnreset(ctx, member: discord.Member):
    warns[member.id] = 0
    await ctx.send(f"🔁 Les warns de {member.mention} ont été réinitialisés.")

@bot_protect.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member):
    await warn_user(member, ctx.channel, "Warn manuel")

@bot_protect.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"🔊 {member.mention} a été unmute.")
    else:
        await ctx.send("❌ Rôle Muted introuvable.")

############################################################
#              LANCEMENT DU BOT
############################################################

TOKEN = os.getenv("TOKEN1")
bot_protect.run(TOKEN)
