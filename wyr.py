import os
import certifi
import discord
from discord.ext import commands, tasks

os.environ['SSL_CERT_FILE'] = certifi.where()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")
    if not update_bot_status.is_running():
        update_bot_status.start()

@tasks.loop(minutes=5)
async def update_bot_status():
    num_servers = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.listening, name=f"{num_servers} servers | !wyrhelp")
    await bot.change_presence(activity=activity)

@bot.command(name="wyrhelp")
async def help_command(ctx):
    await ctx.message.delete()
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=1102829137456017460&permissions=8&scope=bot"
    official_server_link = "https://discord.gg/k78zqRjRFh"
    help_message = (f"**Would You Rather Bot**\n"
                    "Created by kusuri\n\n"
                    f"Invite link: {invite_link}\n"
                    f"Official server: {official_server_link}\n\n"
                    "Usage:\n"
                    "1. Type `!wyr <option1> <option2>` in a channel that starts with 'wyr'.\n"
                    "2. Users can react with 1️⃣ or 2️⃣ to vote on their preference.")
    await ctx.author.send(help_message)

@bot.command()
async def wyr(ctx, option1: str = None, option2: str = None):
    if not ctx.channel.name.startswith("wyr"):
        await ctx.send(f"Please use the `!wyr` command in a channel that starts with 'wyr'. Example: #wyr-channel", delete_after=10)
        return

    if option1 is None or option2 is None:
        await ctx.send("Please provide two options for the `!wyr` command. Example: !wyr pizza pasta", delete_after=10)
        return

    await ctx.message.delete()

    embed = discord.Embed(title="Would you rather...",
                          description=f"1️⃣ {option1}\n\nor\n\n2️⃣ {option2}",
                          color=discord.Color.blue())

    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

    # Create a thread for comments
    thread = await message.create_thread(name=f"WYR {option1} or {option2}", auto_archive_duration=1440)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!wyr') and message.channel.name.startswith("wyr"):
        await bot.process_commands(message)
    elif message.channel.name.startswith("wyr"):
        await message.delete()
        await message.author.send("Only !wyr commands are allowed in this channel. Please use the correct format: !wyr <option1> <option2>")
    else:
        await bot.process_commands(message)

bot.run("YOUR_BOT_TOKEN")
