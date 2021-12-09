# Import
from os import name
import discord
from discord.ext import commands
import random
import aiohttp
import json
from datetime import datetime
from pymongo import MongoClient
import requests
import asyncio
from token_var import token

timestamp = int(datetime.now().timestamp())
print(timestamp)


# # Custom Prefixes
# def get_prefix(client, message):  # first we define get_prefix
#     with open('prefixes.json', 'r') as f:  # we open and read the prefixes.json, assuming it's in the same file
#         prefixes = json.load(f)  # load the json as prefixes
#     return prefixes[str(message.guild.id)]  # recieve the prefix for the guild id given


client = commands.Bot(command_prefix=("f!"), help_command=None)


# @client.event
# async def on_guild_join(guild):  # when the bot joins the guild
#     with open('prefixes.json', 'r') as f:  # read the prefix.json file
#         prefixes = json.load(f)  # load the json file

#     prefixes[str(guild.id)] = '?'  # default prefix

#     with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
#         json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater


# @client.event
# async def on_guild_remove(guild):  # when the bot is removed from the guild
#     with open('prefixes.json', 'r') as f:  # read the file
#         prefixes = json.load(f)

#     prefixes.pop(str(guild.id))  # find the guild.id that bot was removed from

#     with open('prefixes.json', 'w') as f:  # deletes the guild.id as well as its prefix
#         json.dump(prefixes, f, indent=4)


# @client.command(pass_context=True)
# @commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
# async def changeprefix(ctx, prefix):  # command: bl!changeprefix ...
#     print("Changeprefix command used")
#     with open('prefixes.json', 'r') as f:
#         prefixes = json.load(f)

#     prefixes[str(ctx.guild.id)] = prefix

#     with open('prefixes.json', 'w') as f:  # writes the new prefix into the .json
#         json.dump(prefixes, f, indent=4)
#         print(f"Prefix changed to {prefix}")

#     await ctx.send(f'Prefix changed to: `{prefix}`')
#     print("Change prefix message sent")  # confirms the prefix it's been changed to
#     # next step completely optional: changes bot nickname to also have prefix in the nickname


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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over Finnair"))

# Commands

# Help message
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help")
    embed.add_field(name="WIP", value="WIP")
    await ctx.reply(embed=embed)

# #Custom messages
# @client.command()
# async def custom_message(message):
#     channel_1 = client.get_channel(894953882424320080)
#     embed=discord.Embed(title="Annoucement!", description="Ping - <@&894557281931391047>")
#     embed.add_field(name="Annoucement signed by Metolix", value="The economy system will be shutdown again cause we need to switch to a database from JSON files. Stay tuned here for more info when the economy system is back. You don't need to worry about your balance it will be backed up.")
#     await channel_1.send(embed=embed)
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
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')
#Ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.ban(member)
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
    quote = get_quote
    embed = discord.Embed(name="Inspirational Quote", color=discord.Color.random())
    embed.add_field(name="Quote - ", value=quote)
    await ctx.reply(embed=embed)

# Economy
@client.command(aliases=["bal"])
@commands.guild_only()
async def balance(ctx):
	user = ctx.author

	await open_bank(user)

	users = await get_bank_data(user)

	wallet_amt = users[0]
	bank_amt = users[1]

	net_amt = int(wallet_amt + bank_amt)

	em = discord.Embed(
			title= f"{user.name}'s Balance",
			description= f"Wallet: {wallet_amt}\nBank: {bank_amt}",
			color=discord.Color(0x00ff00)
		)

	await ctx.send(embed=em)


@client.command(aliases=["with"])
@commands.guild_only()
async def withdraw(ctx, *,amount= None):
    user = ctx.author
    await open_bank(user)

    users = await get_bank_data(user)

    bank_amt = users[1]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, +1*bank_amt)
        await update_bank(user, -1*bank_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {bank_amt} in your wallet")

    amount = int(amount)

    if amount > bank_amt:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, +1 * amount)
    await update_bank(user, -1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")


@client.command(aliases=["dep"])
@commands.guild_only()
async def deposit(ctx, *,amount= None):
    user = ctx.author
    await open_bank(user)

    users = await get_bank_data(user)

    wallet_amt = users[0]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, -1*wallet_amt)
        await update_bank(user, +1*wallet_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {wallet_amt} in your wallet")

    amount = int(amount)

    if amount > wallet_amt:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, -1 * amount)
    await update_bank(user, +1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")
# Bank Funcs
auth_url = "mongodb+srv://Sidhak_3810:<Sidhak@3810>@main.c546s.mongodb.net/Cluster0?retryWrites=true&w=majority"


async def open_bank(user):
    cluster = MongoClient(auth_url)
    db = cluster["Cluster0"]

    cursor = db["main"]

    try:
        post = {"_id": user.id, "wallet": 5000, "bank": 0}

        cursor.insert_one(post)

    except:
        pass


async def get_bank_data(user):
    cluster = MongoClient(auth_url)
    db = cluster["Cluster0"]

    cursor = db["main"]

    user_data = cursor.find({"_id": user.id})

    cols = ["wallet", "bank"]

    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data


async def update_bank(user, amount=0, mode="wallet"):
    cluster = MongoClient(auth_url)
    db = cluster["Cluster0"]

    cursor = db["main"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})
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
client.run(token)