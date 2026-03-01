import discord
from discord import app_commands
from discord.ext import commands, tasks
import sqlite3
import time
import random

# --- CONFIGURATION ---
TOKEN = "YOUR_TOKEN_HERE"  # <--- PASTE YOUR TOKEN HERE
LEADERBOARD_CHANNEL = "🎯-live-leaderboard"

# --- ROLE SHOP CONFIGURATION ---
ROLE_SHOP = {
    "Bronze Knight":    {"cost": 500,    "role_id": 1178053032987078717},
    "Silver Commander": {"cost": 1500,   "role_id": 1476989179882639502},
    "Gold Legend":      {"cost": 5000,   "role_id": 1476989448062238954},
    "Admin":            {"cost": 100000, "role_id": 1476989665188778014}
}

# --- SETUP ---
class NavyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("Bot is starting...")

bot = NavyBot()

# Database
conn = sqlite3.connect('levels.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER, coins INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS daily_claims (user_id INTEGER PRIMARY KEY, last_claim REAL)''')
conn.commit()

# Variables
voice_sessions = {}
prank_usage = {}  # Stores how many times someone tried the glitch
XP_PER_MESSAGE = 5
XP_PER_MINUTE_VOICE = 2
COINS_PER_LEVEL_UP = 50

# --- HELPER FUNCTIONS ---
def get_user_data(user_id):
    c.execute("SELECT xp, level, coins FROM users WHERE user_id = ?", (user_id,))
    return c.fetchone()

def update_user_data(user_id, xp, level, coins):
    c.execute("INSERT OR REPLACE INTO users (user_id, xp, level, coins) VALUES (?, ?, ?, ?)", (user_id, xp, level, coins))
    conn.commit()

def add_xp(user_id, amount):
    data = get_user_data(user_id)
    if data is None:
        xp, level, coins = 0, 0, 0
    else:
        xp, level, coins = data

    new_xp = xp + amount
    next_level_xp = 100 * ((level + 1) ** 2)
    leveled_up = False
    
    if new_xp >= next_level_xp:
        level += 1
        coins += COINS_PER_LEVEL_UP 
        leveled_up = True
    
    update_user_data(user_id, new_xp, level, coins)
    return new_xp, level, coins, leveled_up

# --- ADMIN COMMANDS ---
@bot.command()
async def sync(ctx):
    await ctx.send("⏳ Syncing commands...")
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Synced {len(synced)} commands!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def clearsync(ctx):
    bot.tree.clear_commands(guild=ctx.guild)
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send("🧹 Duplicates cleaned!")

# --- THE PRANK COMMAND (DEVELOPER) ---
@bot.tree.command(name="developer", description="⚠️ Access Developer Tools (Admin Only)")
async def developer(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    # Get how many times they used it (default 0)
    count = prank_usage.get(user_id, 0) + 1
    prank_usage[user_id] = count

    if count < 5:
        remaining = 5 - count
        # THE COUNTDOWN MESSAGE
        await interaction.response.send_message(f"⚠️ **ACCESS RESTRICTED:** Developer Tools (Admin Only) \n\n🔰 **Verification Required:** Run this command **{remaining} more times** to confirm Admin privileges.", ephemeral=True)
    else:
        # THE REVEAL (The GIF)
        await interaction.response.send_message("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWR4MGlpZDVvbzg2aml1azd1ODNqZm1kZHhzZTVsNWJ4aTZmYzU5eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IfPE0x5gfa5ctKpph6/giphy.gif")
        # Reset count so they can get pranked again later
        prank_usage[user_id] = 0

# --- STANDARD SLASH COMMANDS ---
@bot.tree.command(name="rank", description="Check rank for yourself or another user")
@app_commands.describe(member="Select a user to check their stats")
async def rank(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    data = get_user_data(target.id)
    if data:
        xp, level, coins = data
        embed = discord.Embed(title=f"🛡️ Rank Card: {target.display_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="XP", value=str(xp), inline=True)
        embed.add_field(name="Coins", value=f"🪙 {coins}", inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        msg = "They haven't earned any XP yet!" if member else "You haven't earned any XP yet!"
        await interaction.response.send_message(msg, ephemeral=True)

@bot.tree.command(name="daily", description="Claim your 50 free daily coins.")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    c.execute("SELECT last_claim FROM daily_claims WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    now = time.time()
    
    if result and (now - result[0]) < 86400:
        remaining = int(86400 - (now - result[0])) // 3600
        await interaction.response.send_message(f"⏳ Please wait {remaining} more hours to claim your daily reward.", ephemeral=True)
    else:
        reward = 50
        data = get_user_data(user_id)
        if data:
            xp, level, coins = data
            update_user_data(user_id, xp, level, coins + reward)
        else:
            update_user_data(user_id, 0, 0, reward)
        
        c.execute("INSERT OR REPLACE INTO daily_claims (user_id, last_claim) VALUES (?, ?)", (user_id, now))
        conn.commit()
        await interaction.response.send_message(f"💰 **{reward} Coins** added to your wallet! Come back tomorrow.")

@bot.tree.command(name="shop", description="View the role shop and prices.")
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(title="🛒 Navy Knights Role Shop", description="Buy roles with your hard-earned Coins!", color=discord.Color.gold())
    for role_name, details in ROLE_SHOP.items():
        embed.add_field(name=f"{role_name}", value=f"🪙 {details['cost']} Coins", inline=False)
    embed.set_footer(text="Use /buy to purchase a role!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy", description="Purchase a role from the shop.")
@app_commands.choices(role_name=[
    app_commands.Choice(name="Bronze Knight (500 Coins)", value="Bronze Knight"),
    app_commands.Choice(name="Silver Commander (1500 Coins)", value="Silver Commander"),
    app_commands.Choice(name="Gold Legend (5000 Coins)", value="Gold Legend"),
    app_commands.Choice(name="Admin (100,000 Coins)", value="Admin")
])
async def buy(interaction: discord.Interaction, role_name: app_commands.Choice[str]):
    selected_role = role_name.value
    role_info = ROLE_SHOP.get(selected_role)
    data = get_user_data(interaction.user.id)
    if not data:
        await interaction.response.send_message("❌ You don't have any coins yet.", ephemeral=True)
        return
        
    xp, level, coins = data
    cost = role_info['cost']
    if coins < cost:
        await interaction.response.send_message(f"❌ You need **{cost - coins}** more coins to buy this!", ephemeral=True)
        return
    
    role = interaction.guild.get_role(role_info['role_id'])
    if not role:
        await interaction.response.send_message("⚠️ Error: Role not found. Contact Admin.", ephemeral=True)
        return

    if role in interaction.user.roles:
        await interaction.response.send_message("✅ You already have this role!", ephemeral=True)
        return

    try:
        await interaction.user.add_roles(role)
        update_user_data(interaction.user.id, xp, level, coins - cost)
        await interaction.response.send_message(f"🎉 Purchased **{selected_role}** for {cost} coins!")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission! Move my bot role higher.", ephemeral=True)

@bot.tree.command(name="gamble", description="Bet your coins to win double or nothing!")
async def gamble(interaction: discord.Interaction, amount: int):
    data = get_user_data(interaction.user.id)
    if not data: 
        await interaction.response.send_message("You have 0 coins!", ephemeral=True)
        return
    xp, level, coins = data
    if amount > coins:
        await interaction.response.send_message("❌ You don't have enough coins!", ephemeral=True)
        return
    if amount < 10:
        await interaction.response.send_message("❌ Minimum bet is 10 coins.", ephemeral=True)
        return

    if random.choice([True, False]):
        new_coins = coins + amount
        result = f"✅ You WON! You gained {amount} coins."
        color = discord.Color.green()
    else:
        new_coins = coins - amount
        result = f"📉 You lost {amount} coins."
        color = discord.Color.red()
        
    update_user_data(interaction.user.id, xp, level, new_coins)
    embed = discord.Embed(title="🎲 High Stakes Gamble", description=result, color=color)
    embed.add_field(name="New Balance", value=f"🪙 {new_coins}")
    await interaction.response.send_message(embed=embed)

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    update_leaderboard.start()

@bot.event
async def on_message(message):
    if message.author.bot: return

    xp, level, coins, leveled_up = add_xp(message.author.id, XP_PER_MESSAGE)
    
    if random.randint(1, 20) == 1:
        coins += 10
        update_user_data(message.author.id, xp, level, coins)
        await message.add_reaction("🪙")

    if leveled_up:
        channel = discord.utils.get(message.guild.text_channels, name="achievements")
        if channel:
            await channel.send(f"🎉 {message.author.mention} reached **Level {level}** and earned **{COINS_PER_LEVEL_UP}** coins!")
        try:
            await message.author.send(f"🔥 Congratulations on reaching Level {level} in {message.guild.name}!")
        except:
            pass

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    if before.channel is None and after.channel is not None:
        voice_sessions[member.id] = time.time()
    elif before.channel is not None and after.channel is None:
        if member.id in voice_sessions:
            join_time = voice_sessions.pop(member.id)
            duration_minutes = int((time.time() - join_time) / 60)
            if duration_minutes > 0:
                xp_earned = duration_minutes * XP_PER_MINUTE_VOICE
                add_xp(member.id, xp_earned)

@tasks.loop(minutes=5)
async def update_leaderboard():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=LEADERBOARD_CHANNEL)
        if channel:
            c.execute("SELECT user_id, level, xp, coins FROM users ORDER BY level DESC, xp DESC LIMIT 10")
            top_users = c.fetchall()
            embed = discord.Embed(title="🏆 Navy Knights Live Leaderboard", color=discord.Color.gold())
            description = ""
            for index, user_data in enumerate(top_users):
                user_id, level, xp, coins = user_data
                member = guild.get_member(user_id)
                name = member.display_name if member else "Unknown Knight"
                medal = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else f"#{index+1}"
                description += f"**{medal} {name}**\nLevel {level} • {xp} XP • 🪙 {coins}\n\n"
            
            embed.description = description
            embed.set_footer(text="Updates every 5 minutes")
            async for message in channel.history(limit=5):
                if message.author == bot.user:
                    await message.edit(embed=embed)
                    break
            else:
                await channel.send(embed=embed)

bot.run('')

