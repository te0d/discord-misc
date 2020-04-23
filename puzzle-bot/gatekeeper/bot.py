import argparse
import config
import logging

from discord.ext import commands

parser = argparse.ArgumentParser(description="Run a chatterbot discord bot")
parser.add_argument("--verbose", "-v", action="count", help="logging verbosity")
cliArgs = parser.parse_args()

loggingLevel = "WARNING"
if cliArgs.verbose == 1:
    loggingLevel = "INFO"
elif cliArgs.verbose == 2:
    loggingLevel = "DEBUG"

logging.basicConfig(level=loggingLevel)
logging.info("Logging level set to '{0}'.".format(loggingLevel))

bot = commands.Bot(command_prefix="papa, ")
awaitingResponses = {}

@bot.listen()
async def on_member_join(member):
    awaitingResponses[member.name] = {
        "stage": "welcome",
        "count": 0
    }
    await member.guild.system_channel.send("WHO GOES THERE?")

@bot.listen()
async def on_message(message):
    if message.author.name in awaitingResponses:
        context = awaitingResponses[message.author.name]
        stage = context["stage"]
        context["count"] += 1
        count = context["count"]

        if stage == "welcome" and message.content.isupper():
            for role in message.guild.roles:
                if role.name == "neophyte":
                    neophyte_role = role
            await message.author.edit(nick="BOB", roles=[neophyte_role])
            await message.channel.send("WELL ALRIGHT THEN, BOB! COME ON IN.")
        elif stage == "welcome" and count == 2:
            await message.channel.send("I CAN'T HEAR YOU! YOU NEED TO SPEAK LOUDER!")
        elif stage == "welcome" and count < 3:
            await message.channel.send("WHAT? I CAN'T HEAR YOU!")
        elif stage == "welcome":
            await message.channel.send("YOU NEED TO SPEAK UP.")
            await message.channel.send("/me boots the 呆子 out")
            await message.author.kick(reason="YOU NEED TO SPEAK UP.")

@bot.command()
async def say(ctx, *, args):
    await ctx.send(args[:256].capitalize())

@bot.command()
async def spawn(ctx, spawn_type, *, args):
    if ctx.guild:
        await ctx.guild.create_text_channel(args[:64])

bot.run(config.token)
