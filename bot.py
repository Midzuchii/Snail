import discord
from discord.ext import commands
import datetime
from decouple import config  # Import the config function from python-decouple

# Load the bot token from the .env file
TOKEN = config('TOKEN')

# Prefix for bot commands
PREFIX = "!"

# Create a bot instance with a specified command prefix
bot = commands.Bot(command_prefix=PREFIX)

# Variable to store the bot's start time
bot.start_time = None

# Event: Bot is ready
@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Command: User registration
@bot.command()
async def register(ctx, unique_id):
    # Check if the user has the "Mod" role (customize role name as needed)
    if "Mod" in [role.name for role in ctx.author.roles]:
        # Add user registration logic here (e.g., store unique_id in a database)
        await ctx.send(f"User {ctx.author.name} registered with Unique ID: {unique_id}")
    else:
        await ctx.send("Only moderators can register users.")

# Command: Approve user registration
@bot.command()
async def approve(ctx, user: discord.Member):
    # Check if the user has the "Mod" role (customize role name as needed)
    if "Mod" in [role.name for role in ctx.author.roles]:
        # Add user approval logic here (e.g., assign a custom role)
        role = discord.utils.get(ctx.guild.roles, name="Super Snail")
        await user.add_roles(role)
        await ctx.send(f"Approved user {user.name}.")
    else:
        await ctx.send("Only moderators can approve users.")

# Command: Send feedback
@bot.command()
async def feedback(ctx, *, message):
    # Add feedback handling logic here (e.g., store feedback in a database)
    # In this example, we'll print the feedback to the console and send a confirmation message
    print(f"Feedback received from {ctx.author.name}: {message}")
    await ctx.send("Thank you for your feedback!")

# Command: Bot uptime
@bot.command()
async def uptime(ctx):
    # Calculate uptime based on bot's start time
    if bot.start_time is not None:
        uptime_seconds = (datetime.datetime.utcnow() - bot.start_time).total_seconds()
        # Format uptime into a human-readable string
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        await ctx.send(f"Bot uptime: {uptime_str}")
    else:
        await ctx.send("Bot start time not set. Bot may not be ready yet.")

# Run the bot with the specified token
bot.run(TOKEN)