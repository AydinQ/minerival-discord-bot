import discord
from discord.ext import commands
from discord import app_commands
import random, aiohttp, asyncio

# ---------------- CONFIG ----------------
import os
TOKEN = os.environ['TOKEN']
GUILD_ID = 1404209672130396221     # Replace with your server ID



# ---------------- INTENTS ----------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # For optional message-based commands
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ---------------- MODERATION COMMANDS ----------------
@tree.command(name="ban", description="Ban a user", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str="No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {member} was banned. Reason: {reason}")

@tree.command(name="kick", description="Kick a user", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str="No reason provided"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 {member} was kicked. Reason: {reason}")

@tree.command(name="mute", description="Temporarily mute a user", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def mute(interaction: discord.Interaction, member: discord.Member, time: int):
    role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not role:
        role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await interaction.response.send_message(f"🔇 {member} muted for {time} minutes")
    await asyncio.sleep(time * 60)
    await member.remove_roles(role)

@tree.command(name="unmute", description="Unmute a user", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    role = discord.utils.get(interaction.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await interaction.response.send_message(f"🔊 {member} was unmuted")

@tree.command(name="warn", description="Warn a user", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str="No reason provided"):
    await interaction.response.send_message(f"⚠️ {member} has been warned. Reason: {reason}")

@tree.command(name="purge", description="Delete multiple messages", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def purge(interaction: discord.Interaction, number: int):
    await interaction.channel.purge(limit=number)
    await interaction.response.send_message(f"🧹 Deleted {number} messages", ephemeral=True)

# ---------------- FUN COMMANDS ----------------
@tree.command(name="coinflip", description="Flip a coin", guild=discord.Object(id=GUILD_ID))
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Heads", "Tails"]))

@tree.command(name="rps", description="Play rock-paper-scissors", guild=discord.Object(id=GUILD_ID))
async def rps(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Rock", "Paper", "Scissors"]))

@tree.command(name="meme", description="Fetch a meme", guild=discord.Object(id=GUILD_ID))
async def meme(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as r:
            data = await r.json()
            await interaction.response.send_message(data["url"])

@tree.command(name="dice", description="Roll a dice with X sides", guild=discord.Object(id=GUILD_ID))
async def dice(interaction: discord.Interaction, sides: int = 6):
    await interaction.response.send_message(f"🎲 Rolled: {random.randint(1, sides)}")

@tree.command(name="trivia", description="Random trivia question", guild=discord.Object(id=GUILD_ID))
async def trivia(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://opentdb.com/api.php?amount=1&type=boolean") as r:
            data = await r.json()
            q = data['results'][0]['question']
            await interaction.response.send_message(f"❓ {q}")

# ---------------- INFO COMMANDS ----------------
@tree.command(name="userinfo", description="Show Discord info about a user", guild=discord.Object(id=GUILD_ID))
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined", value=member.joined_at)
    embed.set_thumbnail(url=member.avatar)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serverinfo", description="Show server info", guild=discord.Object(id=GUILD_ID))
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}")
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Boosts", value=guild.premium_subscription_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    await interaction.response.send_message(embed=embed)

@tree.command(name="avatar", description="Show user avatar", guild=discord.Object(id=GUILD_ID))
async def avatar(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.avatar)

# ---------------- UTILITY COMMANDS ----------------
@tree.command(name="ping", description="Show bot latency", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency*1000)}ms")

@tree.command(name="say", description="Bot repeats your message", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# ---------------- GIVEAWAY / COMMUNITY COMMANDS ----------------
@tree.command(name="giveaway", description="Start a giveaway", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def giveaway(interaction: discord.Interaction, prize: str, duration: int):
    embed = discord.Embed(title="🎉 Giveaway!", description=f"Prize: **{prize}**\nDuration: {duration} minutes")
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction("🎉")
    await interaction.response.send_message("Giveaway started! 🎁", ephemeral=True)
    await asyncio.sleep(duration * 60)
    new_msg = await interaction.channel.fetch_message(msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users) if users else None
    if winner:
        await interaction.channel.send(f"🎊 Congrats {winner.mention}, you won {prize}!")
    else:
        await interaction.channel.send("No participants in the giveaway.")

# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Logged in as {bot.user}")
    print("Slash commands registered:")
    for command in tree.get_commands():
        print(command.name)

bot.run(TOKEN)
