# Import
import random
import aiohttp
import json
from datetime import datetime
from discord import embeds
import requests

import discord
from discord.ext import commands
from discord.message import Message

from token_var import token

timestamp = int(datetime.now().timestamp()) # printing time
print(timestamp)

client = commands.Bot(command_prefix=("f!"), help_command=None) # initializing bot

# sends the prefix when @mentioned
@client.event 
async def on_message(msg):
    if msg.mentions[0] == client.user:
        print("The bot was mentioned")
        await msg.channel.send(f"My prefix is `f!`")
    await client.process_commands(msg)


# Startup
@client.event
async def on_ready():
    print("Ready")
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over Finnair"))

# Help command
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="hey")
    embed.add_field(name="WIP", value="WIP")
    await ctx.send(embed=embed)

# Commands
# Custom message
@client.command()
@commands.has_permissions(administrator=True)
async def custom_msg(ctx, *, channel : discord.TextChannel, text=None):
    await ctx.channel.send(text)

#Seats - WIP
@client.command()
async def seats(ctx):
    embed = discord.Embed(title="How to get seats")
    embed.add_field(name="Tutorial - ", value="First you buy the seat by saying `f!buy [seat]` you can see the seats by typing `f!shop`. Now buy the seat and go to <#917329394039656449> and send your picture of the bag. To get the bag type `f!bag`. Only do this if you have purchased the seat you want.")
    await ctx.reply(embed=embed)

# Ping
@client.command()
async def ping(ctx):
    print("Ping command used")
    latency = round(client.latency * 1000) # gets client latency
    print(f"Got the latency: {latency}")
    embed = discord.Embed(title="Ping command.", description="Tells the latency of the bot.")
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
                           description="Gets a random meme.",
                           color=discord.Colour.random())

    async with aiohttp.ClientSession() as cs: # initialize http session
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r: #get r/dankmemes
            res = await r.json()
            print("Got the meme")
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url']) # strip the json
            await ctx.send(embed=embed)
            print("Meme sent")

# Kick command
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == None:
        await ctx.send(embed=discord.Embed(description='You have to supply a user!')) 
        return
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member, reason=reason + ' Moderator: {0}'.format(ctx.author))
    await ctx.send(embed=discord.Embed(description='User {0} has been kicked!\nReason: {1}'.format(member.mention, reason)))

#Ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == None:
        await ctx.send(embed=discord.Embed(description='You have to supply a user!'))
        return
    if reason==None:
        reason=" no reason provided"
    await ctx.guild.ban(member, reason=reason + ' Moderator: {0}'.format(ctx.author))
    await ctx.send(embed=discord.Embed(description='User {0} has been banned!\nReason: {1}'.format(member.mention, reason)))

#Avatar
@client.command(aliases=["av", "Av", "AV", "aV"]) # aliases for some reason
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        await ctx.reply(ctx.message.author.avatar)
    else:
        await ctx.reply(member.avatar)

# Inspire
def get_quote():
    response = requests.get("https://zenquotes.io/api/random") # queries api
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a'] # strips json
    return(quote)

@client.command()
async def inspire(ctx):
    quote = get_quote()
    embed = discord.Embed(title="Inspirational Quote", color=discord.Color.random())
    embed.add_field(name="Quote - ", value=quote)
    embed.add_field(name="Quotes provided by ZenQuotes", value="https://zenquotes.io (Not sponsered)")
    await ctx.reply(embed=embed)

# Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Command not found :/ Use `f!help` for more info on commands.")
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(embed=discord.Embed(description='You do not have sufficient permissions!'))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(embed=discord.Embed(description="Woah! Command still on cooldown for {:.2f} seconds.".format(error.retry_after)))


@age.error
async def age_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply(embed=discord.Embed(description="Please make sure you are using an integer."))

# Run
client.run(token)