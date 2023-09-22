import discord
from discord.ext import commands
import datetime
from decouple import config

# Use the `config` function from decouple to read the TOKEN from the .env file
TOKEN = config('TOKEN')
PREFIX = "!"

# Define your bot's intents
intents = discord.Intents.default()
intents.typing = False  # Disable typing notifications, if desired
intents.presences = False  # Disable presence updates, if desired
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.start_time = None

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Set the bot's status to "online"
    await bot.change_presence(status=discord.Status.online)

@bot.command()
async def register(ctx, unique_id):
    # Check if the user has the "Mod" or "Owner" role
    mod_role = discord.utils.get(ctx.guild.roles, name="Mod")
    owner_role = discord.utils.get(ctx.guild.roles, name="Owner")

    if mod_role in ctx.author.roles or owner_role in ctx.author.roles:
        # Rest of your code for registration
        # ...
    else:
        await ctx.send("Only moderators and the owner can register users.")

@bot.command()
async def approve(ctx, user: discord.Member):
    # Check if the user has the "Mod" or "Owner" role
    mod_role = discord.utils.get(ctx.guild.roles, name="Mod")
    owner_role = discord.utils.get(ctx.guild.roles, name="Owner")

    if mod_role in ctx.author.roles or owner_role in ctx.author.roles:
        # Rest of your code for approval
        # ...
    else:
        await ctx.send("Only moderators and the owner can approve users.")

@bot.command()
async def feedback(ctx, *, message):
    print(f"Feedback received from {ctx.author.name}: {message}")
    await ctx.send("Thank you for your feedback!")

@bot.command()
async def uptime(ctx):
    if bot.start_time is not None:
        uptime_seconds = (datetime.datetime.utcnow() - bot.start_time).total_seconds()
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        await ctx.send(f"Bot uptime: {uptime_str}")
    else:
        await ctx.send("Bot start time not set. Bot may not be ready yet.")

bot.run(TOKEN)