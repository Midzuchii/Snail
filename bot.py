import os
import discord
from discord.ext import commands
import datetime
from decouple import config

api_key = os.environ['asRuCUrqDVpAfmNUNRSynQaYC6xw6yFcTJbzCNpm']
TOKEN = config('TOKEN')
PREFIX = "!"
bot = commands.Bot(command_prefix=PREFIX)
bot.start_time = None

# Check if the API key is set
if api_key is None:
    print("API_KEY environment variable is not set.")
else:
    print(f"API_KEY: {api_key}")


@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Set the bot's status to "online"
    await bot.change_presence(status=discord.Status.online)

@bot.command()
async def register(ctx, unique_id):
    if "Mod" in [role.name for role in ctx.author.roles]:
        await ctx.send(f"User {ctx.author.name} registered with Unique ID: {unique_id}")
    else:
        await ctx.send("Only moderators can register users.")

@bot.command()
async def approve(ctx, user: discord.Member):
    if "Mod" in [role.name for role in ctx.author.roles]:
        role = discord.utils.get(ctx.guild.roles, name="Super Snail")
        await user.add_roles(role)
        await ctx.send(f"Approved user {user.name}.")
    else:
        await ctx.send("Only moderators can approve users.")

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
