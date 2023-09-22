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
owner_id = 270254006096494592  # Replace with your owner's user ID
log_channel_id = 1154795053592612895  # Replace with your log channel ID
waiting_channel_name = "waiting"  # Replace with your waiting channel name
registration_log_channel_id = 1154811703125627012  # Replace with your registration log channel ID

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Set the bot's status to "online"
    await bot.change_presence(status=discord.Status.online)

    owner = await bot.fetch_user(owner_id)  # Fetch the owner's user object
    if owner:
        notification_message = "Bot is now online and ready."
        await owner.send(notification_message)
    else:
        print(f"Owner with ID {owner_id} not found or unavailable.")

@bot.command()
async def register(ctx, unique_id):
    # Check if the user is a moderator or the owner
    if "Mod" in [role.name for role in ctx.author.roles] or ctx.author.id == owner_id:
        # Log the registration request
        log_channel = bot.get_channel(log_channel_id)
        registration_log_channel = bot.get_channel(registration_log_channel_id)  # Replace with your registration log channel ID

        if log_channel and registration_log_channel:
            log_message = f"Registration request from {ctx.author.name} (ID: {ctx.author.id}) with unique ID: {unique_id}"
            await log_channel.send(log_message)

            # Send registration log to the registration log channel
            await registration_log_channel.send(log_message)

            # Notify moderators and owner
            owner = await bot.fetch_user(owner_id)  # Fetch the owner's user object
            moderators = [member for member in ctx.guild.members if "Mod" in [role.name for role in member.roles]]
            notification_message = f"New registration request from {ctx.author.mention} with unique ID: {unique_id}."

            # Send notifications
            await owner.send(notification_message)
            for moderator in moderators:
                await moderator.send(notification_message)

            # Move the user to the waiting channel
            waiting_channel = discord.utils.get(ctx.guild.text_channels, name=waiting_channel_name)
            if waiting_channel:
                await ctx.author.move_to(waiting_channel)
                await ctx.send(f"Registration request sent for approval. You are now in the {waiting_channel.mention} channel.")
            else:
                await ctx.send("Registration log channel not found. Please set it up.")
        else:
            await ctx.send("Registration log channels not found. Please set them up.")
    else:
        await ctx.send("Only moderators and the owner can register users.")

@bot.command()
async def approve(ctx, user: discord.Member):
    if "Mod" in [role.name for role in ctx.author.roles] or ctx.author.id == owner_id:
        # Add your approval logic here
        # Log the approval action if needed
        await ctx.send(f"Approved user {user.name}.")
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
