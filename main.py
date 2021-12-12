# Import
import discord
from discord.ext import commands
import random
import aiohttp
import json
from datetime import datetime
from discord.message import Message
import requests

timestamp = int(datetime.now().timestamp())
print(timestamp)

client = commands.Bot(command_prefix=("f!"), help_command=None)

@client.event
async def on_message(msg):
    try:
        if msg.mentions[0] == client.user:
            print("The bot was mentioned")
            # with open("prefixes.json", "r") as f:
            #     prefixes = json.load(f)
            # pre = prefixes[str(msg.guild.id)]

            await msg.channel.send(f"My prefix is `f!`")
            # print(f"Prefix for {msg.guild.id} is {pre} and was given.")

    except:
        pass
    await client.process_commands(msg)


# Startup
@client.event
async def on_ready():
    print("Ready")
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over Finnair"))

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help")
    embed.add_field(name="WIP", value="WIP")
    await ctx.send(embed=embed)

# Methods

# Used for constructing an embed on the fly
def embed_construct(title: str, message: str):
    em_out = discord.Embed(title=title) 
    em_out.add_field(value=message)

# Commands
# Custom message
@client.command()
@commands.has_permissions(administrator=True)
async def custom_msg(ctx, *, channel : discord.TextChannel, text=None):
    await ctx.channel.send(text)

#Seats
@client.command()
async def seats(ctx):
    embed = discord.Embed(title="How to get seats")
    embed.add_field(name="Tutorial - ", value="First you buy the seat by saying `f!buy [seat]` you can see the seats by typing `f!shop`. Now buy the seat and go to <#917329394039656449> and send your picture of the bag. To get the bag type `f!bag`. Only do this if you have purchased the seat you want.")
    await ctx.reply(embed=embed)
# Ping
@client.command()
async def ping(ctx):
    print("Ping command used")
    latency = round(client.latency * 1000)
    print(f"Got the latency: {latency}")
    embed = discord.Embed(title="Ping command.", description="Tells the latency of the bot.",
                           color=discord.Color.random())
    embed.add_field(name="Pong!", value=f"Latency: {latency}")
    await ctx.reply(embed=embed)
    print("Ping sent")

# Age command
@client.command()
async def age(ctx, year=None):
    if year == None:
        await ctx.reply("Add in what year were you born in...")
        print("User did not enter the year they were bron in")
        return ()
    elif int(year) > 2021:
        await ctx.reply("That age is not possible, bruh.")
        print("The user added an age which was not possible")
        return ()
    elif int(year) == 2021:
        await ctx.reply("Your 0? Get off **DISCORD** NOW!")
        print("The user was 0")
        return ()

    age = 2021 - int(year)
    embed = discord.Embed(title="Age command", description="Tells the age with the year they are born",
                           color=discord.Colour.random())
    embed.add_field(name=f"Year Given : {year}", value=f"They shall be {age} years old.")
    await ctx.reply(embed=embed)
    print(f"The year was {year}. And their age was {age}. Age sent.")


# Time
@client.command()
async def time(ctx):
    await ctx.reply(f"<t:{timestamp}:F>")
    print("Time sent")


# Meme
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="Meme command",
                           description="Get a random meme, WARNING: **WE DON'T MAKE THE MEMES, IF YOU GET ANY NSFW WE ARE NOT RESPONSIBLE**",
                           color=discord.Colour.random())

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            print("Got the meme")
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            print("Meme sent")

# Kick command
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')
#Ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason==None:
        reason=" no reason provided"
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')

#Avatar
@client.command(aliases=["av", "Av", "AV", "aV"])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        await ctx.reply(ctx.message.author.avatar)
    else:
        await ctx.reply(member.avatar)

# Inspire
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)
@client.command()
async def inspire(ctx):
    await ctx.reply("The API has some problems getting the quote, The messages may appear slow.")
    quote = get_quote()
    embed = discord.Embed(title="Inspirational Quote", color=discord.Color.random())
    embed.add_field(name="Quote - ", value=quote)
    embed.add_field(name="Quotes provided by ZenQuotes", value="https://zenquotes.io (Not sponsered)")
    await ctx.reply(embed=embed)

# Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        pre = prefixes[str(ctx.guild.id)]
        await ctx.reply(f"Command not found :/ Use `{pre}help` for more info on commands.")
        print("Invalid command used, command not found")
        return ()
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("Imagine having no perms, 🤣")
        print(f"The user does not have the permissions")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply("Calm down buddy. The command you are using is still on **cooldown**.Try again in {:.2f}s".format(error.retry_after))


@age.error
async def age_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply("Please make sure you are using an integer.")


# Run
client.run("OTE1OTExNDM3NjM1OTQ0NDY4.Yaie_w.U87lcxWdojlRMLgau8mofBsZ2rE")