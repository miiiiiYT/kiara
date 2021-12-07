# Import
import discord as nextcord
from discord.ext import commands
import random
import aiohttp
import json
from datetime import datetime

timestamp = int(datetime.now().timestamp())
print(timestamp)


# Custom Prefixes
def get_prefix(client, message):  # first we define get_prefix
    with open('prefixes.json', 'r') as f:  # we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f)  # load the json as prefixes
    return prefixes[str(message.guild.id)]  # recieve the prefix for the guild id given


client = commands.Bot(
    command_prefix=(get_prefix),
)


@client.event
async def on_guild_join(guild):  # when the bot joins the guild
    with open('prefixes.json', 'r') as f:  # read the prefix.json file
        prefixes = json.load(f)  # load the json file

    prefixes[str(guild.id)] = '?'  # default prefix

    with open('prefixes.json', 'w') as f:  # write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4)  # the indent is to make everything look a bit neater


@client.event
async def on_guild_remove(guild):  # when the bot is removed from the guild
    with open('prefixes.json', 'r') as f:  # read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))  # find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f:  # deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
async def changeprefix(ctx, prefix):  # command: bl!changeprefix ...
    print("Changeprefix command used")
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:  # writes the new prefix into the .json
        json.dump(prefixes, f, indent=4)
        print(f"Prefix changed to {prefix}")

    await ctx.send(f'Prefix changed to: `{prefix}`')
    print("Change prefix message sent")  # confirms the prefix it's been changed to
    # next step completely optional: changes bot nickname to also have prefix in the nickname


@client.event
async def on_message(msg):
    try:
        if msg.mentions[0] == client.user:
            print("The bot was mentioned")
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            pre = prefixes[str(msg.guild.id)]

            await msg.channel.send(f"My prefix for this server is `{pre}`")
            print(f"Prefix for {msg.guild.id} is {pre} and was given.")

    except:
        pass
    await client.process_commands(msg)


# Startup
@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(status=nextcord.Status.online, activity=nextcord.Game("Default prefix - ?"))


# Commands
@client.command()
async def seats(ctx):
    embed = nextcord.Embed(title="How to get seats")
    embed.add_field(name="Tutorial - ", value="First you buy the seat by saying `f!buy [seat]` you can see the seats by typing `f!shop`. Now buy the seat and go to <#917329394039656449> and send your picture of the bag. To get the bag type `f!bag`. Only do this if you have purchased the seat you want.")
    await ctx.reply(embed=embed)
# Ping
@client.command()
async def ping(ctx):
    print("Ping command used")
    latency = round(client.latency * 1000)
    print(f"Got the latency: {latency}")
    embed = nextcord.Embed(title="Ping command.", description="Tells the latency of the bot.",
                           color=nextcord.Color.random())
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
    embed = nextcord.Embed(title="Age command", description="Tells the age with the year they are born",
                           color=nextcord.Colour.random())
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
    embed = nextcord.Embed(title="Meme command",
                           description="Get a random meme, WARNING: **WE DON'T MAKE THE MEMES, IF YOU GET ANY NSFW WE ARE NOT RESPONSIBLE**",
                           color=nextcord.Colour.random())

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
async def kick(ctx, member: nextcord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')
#Ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')

#Avatar
@client.command(aliases=["av", "Av", "AV", "aV"])
async def avatar(ctx, member: nextcord.Member = None):
    if member == None:
        await ctx.reply(ctx.message.author.avatar)
    else:
        await ctx.reply(member.avatar)

# Economy
mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Ferrari","price":99999,"description":"Sports Car"},
            {"name":"Premium Economy","price":100,"description":"Sit in Premium Economy Class in flights"},
            {"name":"Bussiness Class","price":150,"description":"Sit in Bussiness Class in flights"},
            {"name":"First Class","price":250,"description":"Sit in First Class in flights"}]


@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = nextcord.Embed(title=f'{ctx.author.name} Balance',color = nextcord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@client.command()
@commands.cooldown(2,200,commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} FinCoins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} FinCoins')


@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} FinCoins')


@client.command(aliases=['sm'])
async def send(ctx,member : nextcord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} FinCoins')


@client.command(aliases=['rb'])
@commands.cooldown(1,200,commands.BucketType.user)
async def rob(ctx,member : nextcord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} FinCoins')


@client.command()
@commands.cooldown(1,200,commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
    em = nextcord.Embed(title = "Shop", description="**Note** - None of the items work, other than the seats, They profit you in flights. Type `f!seats` for more info.")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = nextcord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = nextcord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = nextcord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal

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