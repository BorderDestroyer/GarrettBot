from urllib import response
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from discord import Color
from discord.utils import get
import asyncio

token = 'YOUR_API_KEY'

#sets what the bot is intended for, set to all as default
intents = discord.Intents().all()

#sets the prefix for commands
client = commands.Bot(command_prefix = ["."], intents=intents) 
client.remove_command('help')

#A list of statuses for the bot to cycle between
status = cycle(['Garrett', 'Garretting'])
#moods for garrett to be in for the day
moods = ["happy", "sad", "mad", "bored", "fearful", "lonely"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#runs when the bot is activated
@client.event
async def on_ready(): 
    change_status.start()
    update_mood.start()
    print("Garrett")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#used to check the latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

#allows the 8ball (or ask command) to function
@client.command(aliases=["8ball", "ask"])
async def _8ball(ctx, *, question):
    responses = ["Garrett thinks: **You should go for it!**",
                "Garrett thinks: **Maybe you should think on that a little more.**",
                "Garrett thinks: **No.**",
                "Garrett thinks: **Yes.**",
                "Garrett thinks: **It's' your funeral.**",
                "Garrett has no: **Thoughts, only dance.**",
                "Garrett thinks of bagels while you ask your question.",
                "Garrett thinks: **Without a doubt!**",
                "Garrett thinks: **It is certain!**",
                "Garrett thinks: **Most likely!**",
                "Garrett thinks: **Don't count on it.**",
                "Garrett thinks: **Ask again later, I'm napping.**",
                "garrettdance.mp4",
                "Garrett thinks: **nothing**"]
    response = random.choice(responses)
    
    if response == "garrettdance.mp4":
        await ctx.send(f"{ctx.author.mention}", file=discord.File(r"./garrettdance.mp4"))
    else:
        await ctx.send(f"{ctx.author.mention} {response}")

#the backdoor into the bot that allows you to have the bot send messages to a specific channel
@client.command()
@commands.has_role("mod")
async def sendmsg(ctx, channel, *, message):
    await client.get_channel(int(channel)).send(f"{message}")
    await ctx.send(f"{ctx.author.mention} Your message **{message}** has been sent to channel ID **{channel}**!")

#just has the bot send the gif to the client the command was used
@client.command()
async def GarrettDance(ctx):
    await ctx.send(f"{ctx.author.mention}", file=discord.File(r"./garrettdance.mp4"))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#TASKS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#changes the bots active status every 30 minutes
@tasks.loop(minutes=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#updates the mood of Garrett every day
@tasks.loop(hours=24)
async def update_mood():
    mood = random.choice(moods)
    reason = "There's no particular reason, just because I'm quirky like that."
    if mood == "happy":
        happyReasons = ["My dance moves are killer today!",
                        "There was a butterfly and I chased it across this field! It was fun!",
                        "I made a friend and we danced together for a while!",
                        "There's no particular reason, just because I'm quirky like that."]
        reason = random.choice(happyReasons)
    elif mood == "sad":
        sadReasons = ["I just can't boogy today...",
                      "I ran out of catfood...",
                      "Someone slipped some catnip in my drink last night...",
                      "Etherium is down 24%...",
                      "I gained 3 pounds...",
                      "There's no particular reason, just because I'm quirky like that.",
                      "My favorite toy just broke..."]
        reason = random.choice(sadReasons)
    elif mood == "mad":
        madReasons = ["I LOST ALL MY MONEY IN CRYPTO!",
                      "There's no particular reason, just because I'm quirky like that.",
                      "Dream is too hot...",
                      "This fucking tail behind me won't leave me alone!"]
        reason = random.choice(madReasons)
    elif mood == "bored":
        boredReasons = ["I no longer feel the need to seek entertainment, I stimulated myself too much with 'toys' and 'catnip' that I have lost all sense of joy in life... I've become a hollow shell with no reason whatsoever... I dance, but with no feeling, I boogy, but with no purpose, no intent... What am I? Also there's nothing good on TV...",
                        "I just want to sleep.",
                        "These toys aren't that much fun anymore.",
                        "There's nothing good to watch on TV.",
                        "I can't think of any dance moves to bust it down to."]
        reason = random.choice(boredReasons)
    elif mood == "fearful":
        fearfulReasons = ["There was a dog right outside my door, what the hell!?",
                          "Fucking vacuume, sucky bitch.",
                          "There was a weird snake thing on the ground, it didn't move and smelled like salt. It was scary!"]
        reason = random.choice(fearfulReasons)
    elif mood == "lonely":
        lonelyReasons = ["No one wants to watch me dance...",
                         "The weird giant human thing that lives in my house went to work.",
                         "The other cats scoffed at me when I tried to talk to them..."]
        reason = random.choice(lonelyReasons)
        
    await client.get_channel(1026282390743683215).send(f"""I am feeling **{mood}** today. {reason}""")

#Runs the bot
async def main():
    async with client:
        await client.start(token)

asyncio.run(main())