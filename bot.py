import discord
from discord.ext import commands
import datetime
from decouple import config
import aiohttp
import asyncio

TOKEN = config('TOKEN')
PREFIX = "!"

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.start_time = None
owner_id = 270254006096494592
log_channel_id = 1154795053592612895
waiting_channel_id = 1154816815273357384
registration_log_channel_id = 1154811703125627012

# Dictionary to store user registration data
user_registrations = {}

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(status=discord.Status.online)
    owner = await bot.fetch_user(owner_id)
    if owner:
        notification_message = "Bot is now online and ready."
        await owner.send(notification_message)
    else:
        print(f"Owner with ID {owner_id} not found or unavailable.")

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(status=discord.Status.online)
    owner = await bot.fetch_user(owner_id)
    if owner:
        notification_message = "Bot is now online and ready."
        await owner.send(notification_message)
    else:
        print(f"Owner with ID {owner_id} not found or unavailable.")

@bot.command()
async def register(ctx, unique_id):
    if "Mod" in [role.name for role in ctx.author.roles] or ctx.author.id == owner_id:
        registration_log_channel = bot.get_channel(registration_log_channel_id)
        if registration_log_channel:
            log_message = f"Registration request from {ctx.author.name} (ID: {ctx.author.id}) with unique ID: {unique_id}"
            await registration_log_channel.send(log_message)
            owner = await bot.fetch_user(owner_id)
            moderators = [member for member in ctx.guild.members if "Mod" in [role.name for role in member.roles]]
            notification_message = f"New registration request from {ctx.author.mention} with unique ID: {unique_id}."
            await owner.send(notification_message)
            for moderator in moderators:
                await moderator.send(notification_message)
            user_registrations[ctx.author.id] = unique_id
            waiting_channel = bot.get_channel(waiting_channel_id)
            if waiting_channel:
                await ctx.author.move_to(None)
                await ctx.send(f"Registration request sent for approval. You are now in the {waiting_channel.mention} channel.")
            else:
                await ctx.send("Waiting channel not found. Please set it up.")
        else:
            await ctx.send("Registration log channel not found. Please set it up.")
    else:
        await ctx.send("Only moderators and the owner can register users.")

@bot.command()
async def approve(ctx, user: discord.Member):
    if "Mod" in [role.name for role in ctx.author.roles] or ctx.author.id == owner_id:
        if user.id in user_registrations:
            unique_id = user_registrations[user.id]
            log_channel = bot.get_channel(log_channel_id)
            if log_channel:
                log_message = f"Approved user {user.name}. Unique ID: {unique_id}"
                await log_channel.send(log_message)
            else:
                print("Standard log channel not found. Please set it up.")
            del user_registrations[user.id]
            await ctx.send(log_message)
        else:
            await ctx.send("This user doesn't have a pending registration.")
    else:
        await ctx.send("Only moderators and the owner can approve users.")

@bot.command()
async def feedback(ctx, *, message):
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        log_message = f"Feedback received from {ctx.author.name}: {message}"
        await log_channel.send(log_message)
    else:
        print("Standard log channel not found. Please set it up.")
    await ctx.send("Thank you for your feedback!")

@bot.command()
async def uptime(ctx):
    if bot.start_time is not None:
        uptime_seconds = (datetime.datetime.utcnow() - bot.start_time).total_seconds()
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        await ctx.send(f"Bot uptime: {uptime_str}")
    else:
        await ctx.send("Bot start time not set. Bot may not be ready yet.")

@bot.command()
async def shelp(ctx):
    help_message = (
        "Available commands:\n"
        "!register [unique_id] - Register a user with a unique ID (for moderators and owner).\n"
        "!approve [user_mention] - Approve a registered user (for moderators and owner).\n"
        "!feedback [message] - Send feedback to the bot owner.\n"
        "!uptime - Display bot uptime.\n"
        "!ping - Test latency to selected site\n"
        "!purge - removes chat dialogue\n"
    )
    await ctx.send(help_message)

@bot.command()
async def mute(ctx, member: discord.Member, duration=None, *, reason=None):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="Silly Snail")
        if mute_role:
            await member.add_roles(mute_role, reason=reason)
            await ctx.send(f'Muted {member.mention} for reason: {reason}')
        else:
            await ctx.send("The 'Silly Snail' mute role does not exist.")
    else:
        await ctx.send("You don't have permission to manage roles.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="Silly Snail")
        if mute_role:
            await member.remove_roles(mute_role)
            await ctx.send(f'Unmuted {member.mention}')
        else:
            await ctx.send("The 'Silly Snail' mute role does not exist.")
    else:
        await ctx.send("You don't have permission to manage roles.")

@bot.command()
async def purge(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Purged {amount} messages.", delete_after=5)
    else:
        await ctx.send("You don't have permission to manage messages.")
        
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for the reason: {reason}.")
    else:
        await ctx.send("You don't have permission to kick members.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned for the reason: {reason}.")
    else:
        await ctx.send("You don't have permission to ban members.")

@bot.command()
async def ping(ctx):
    try:
        # Define the number of pings and the delay between pings (in seconds)
        num_pings = 10
        ping_delay = 1  # 1 second delay between pings

        total_latency = 0
        for _ in range(num_pings):
            start_time = datetime.datetime.utcnow()

            async with aiohttp.ClientSession() as session:
                async with session.get("https://lunaors.eu") as response:
                    if response.status == 200:
                        end_time = datetime.datetime.utcnow()
                        latency = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds
                        total_latency += latency
                        await ctx.send(f'Pong! Latency: {latency:.2f} ms')
                    else:
                        await ctx.send('Failed to ping the website.')

            # Introduce a delay before the next ping
            await asyncio.sleep(ping_delay)

        # Calculate and send the average latency
        average_latency = total_latency / num_pings
        await ctx.send(f'Average Latency: {average_latency:.2f} ms')

    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

bot.run(TOKEN)
