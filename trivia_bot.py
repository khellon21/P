import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio
import time
import random
import aiohttp  # For Anime API
import html     # For cleaning text

# --- CONFIGURATION (PRE-FILLED) ---
TOKEN = ""
CHANNEL_ID = 
OWNER_ID = 

# --- REWARDS ---
REWARDS = {1: 200, 2: 100, 3: 50}

# --- CUSTOM GAMING QUESTIONS (Warzone, Minecraft, CoC ONLY) ---
GAMING_QUESTIONS = {
    # WARZONE
    "In Warzone, what is the name of the 1v1 arena you go to when you die?": ["gulag", "the gulag"],
    "Which Warzone map was based on a real city in Ukraine?": ["verdansk"],
    "What is the maximum amount of armor plates you can hold in your satchel in Warzone?": ["8", "eight"],
    "In Warzone, what allows you to hear enemies' death chat?": ["prox chat", "proximity chat"],
    "What is the name of the gas mask that doesn't break in the gas?": ["durable", "durable gas mask", "golden gas mask"],
    
    # MINECRAFT
    "In Minecraft, what mob creeps up on you and explodes?": ["creeper"],
    "What allows you to travel to the Nether in Minecraft?": ["nether portal", "obsidian portal"],
    "Which block is used to craft a Beacon in Minecraft?": ["glass", "obsidian", "nether star"],
    "What is the only ore found in the Ancient Debris of the Nether?": ["netherite"],
    "What food item is used to tame a Wolf in Minecraft?": ["bone", "bones"],
    "Who is the final boss of Minecraft?": ["ender dragon", "the ender dragon"],

    # CLASH OF CLANS
    "In Clash of Clans, what resource is used to upgrade walls?": ["gold", "elixir", "gold and elixir"],
    "What is the name of the Hero unlocked at Town Hall 7?": ["barbarian king"],
    "Which troop in Clash of Clans loves to destroy defenses first and rides a hog?": ["hog rider"],
    "What is the maximum level of a Town Hall (as of 2025)?": ["17", "th17"], 
    "What dark elixir troop splits into smaller versions of itself when it dies?": ["golem", "golemites"]
}

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect('levels.db')
c = conn.cursor()

def add_coins(user_id, amount):
    c.execute("SELECT xp, level, coins FROM users WHERE user_id = ?", (user_id,))
    data = c.fetchone()
    if data:
        xp, level, coins = data
        c.execute("UPDATE users SET coins = ? WHERE user_id = ?", (coins + amount, user_id))
    else:
        c.execute("INSERT INTO users (user_id, xp, level, coins) VALUES (?, ?, ?, ?)", (user_id, 0, 1, amount))
    conn.commit()

async def get_mixed_question():
    """Picks either an Internet Anime Question OR a Custom Game Question."""
    
    # 50% Chance for Anime (API), 50% Chance for Game (Local List)
    choice = random.choice(["anime", "game"])
    
    if choice == "anime":
        # --- FETCH ANIME QUESTION FROM WEB ---
        # Category 31 is Anime & Manga
        url = "https://opentdb.com/api.php?amount=1&category=31&type=multiple"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['results']:
                            q_data = data['results'][0]
                            question = html.unescape(q_data['question'])
                            correct_answer = html.unescape(q_data['correct_answer'])
                            return question, correct_answer, "Anime (Infinite)"
        except Exception as e:
            print(f"API Error: {e}, falling back to local games.")
    
    # --- FETCH GAME QUESTION FROM LOCAL LIST ---
    # We use list(dict.items()) to handle the dictionary correctly
    question_pair = random.choice(list(GAMING_QUESTIONS.items()))
    question = question_pair[0]
    answers = question_pair[1]
    return question, answers, "Gaming (Warzone/MC/CoC)"

@bot.event
async def on_ready():
    print(f'Hybrid Trivia Bot logged in as {bot.user}')

# --- COMMANDS ---
@bot.command()
async def start_trivia(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Only the Owner can start trivia.")
        return
        
    if not trivia_loop.is_running():
        trivia_loop.start()
        await ctx.send("✅ **Hybrid Trivia Online!**\nMix of Infinite Anime & Specific Gaming Questions.")
    else:
        await ctx.send("⚠️ Trivia is already running!")

@bot.command()
async def stop_trivia(ctx):
    if ctx.author.id != OWNER_ID: return
    trivia_loop.cancel()
    await ctx.send("🛑 Trivia stopped.")

# --- MAIN LOOP (30 MINUTES) ---
@tasks.loop(minutes=30)
async def trivia_loop():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ Could not find channel {CHANNEL_ID}")
        return

    # 1. GET QUESTION
    # Note: get_mixed_question returns (Question, Answer(s), Category)
    try:
        q_data = await get_mixed_question()
        if not q_data: return # Safety check
        
        question_text = q_data[0]
        answer_data = q_data[1]
        category = q_data[2]
        
    except Exception as e:
        print(f"Error fetching question: {e}")
        return
    
    # Logic to handle different answer formats (List vs String)
    valid_answers = []
    display_answer = ""
    
    if isinstance(answer_data, list):
        valid_answers = [a.lower() for a in answer_data]
        display_answer = answer_data[0] # The first one is the 'main' answer
    else:
        valid_answers = [answer_data.lower()]
        display_answer = answer_data

    muted_users = []   
    winners = []       
    
    embed = discord.Embed(title=f"❓ TRIVIA TIME: {category}", description=f"**{question_text}**\n\n🏆 **Rewards:**\n🥇 1st: 200 | 🥈 2nd: 100 | 🥉 3rd: 50\n\n⚠️ **One Strike Rule:** Wrong answer = Muted!", color=discord.Color.green())
    await channel.send(embed=embed)

    print(f"[DEBUG] Answer: {valid_answers}") # For you to see in console

    # 2. GAME LOOP (Wait up to 25 mins)
    end_time = time.time() + 1500 

    while time.time() < end_time:
        remaining = end_time - time.time()
        try:
            msg = await bot.wait_for('message', timeout=remaining)

            if msg.author.bot or msg.channel.id != CHANNEL_ID: continue
            if msg.author in muted_users or msg.author in winners: continue

            # --- CHECK ANSWER ---
            user_ans = msg.content.lower().strip()
            
            # Check if user's answer matches ANY valid answer
            is_correct = False
            for va in valid_answers:
                # Exact match OR substring match for long answers
                if user_ans == va or (len(va) > 5 and user_ans in va):
                    is_correct = True
                    break

            if is_correct:
                rank = len(winners) + 1
                reward = REWARDS.get(rank, 0)
                add_coins(msg.author.id, reward)
                winners.append(msg.author)
                
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                await channel.send(f"{medal} **{msg.author.mention}** is {rank} place! (+{reward} Coins)")
                
                if len(winners) >= 3:
                    await channel.send(f"🚫 **Round Locked!** The answer was: **{display_answer}**")
                    break 
            else:
                try:
                    await channel.set_permissions(msg.author, send_messages=False)
                    muted_users.append(msg.author)
                    await msg.add_reaction("❌")
                except:
                    pass

        except asyncio.TimeoutError:
            break

    # 3. CLEANUP
    if len(winners) == 0:
        fail_embed = discord.Embed(title="⏰ TIME'S UP!", description=f"Nobody won.\n**Answer:** {display_answer}", color=discord.Color.red())
        await channel.send(embed=fail_embed)

    if muted_users:
        for user in muted_users:
            try:
                await channel.set_permissions(user, overwrite=None)
            except:
                pass

bot.run(TOKEN)

