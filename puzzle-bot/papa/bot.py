import argparse
import config
import datetime
import logging

import discord

parser = argparse.ArgumentParser(description="Run a chatterbot discord bot")
parser.add_argument("--verbose", "-v", action="count", help="logging verbosity")
cliArgs = parser.parse_args()

logging_level = "WARNING"
if cliArgs.verbose == 1:
    logging_level = "INFO"
elif cliArgs.verbose == 2:
    logging_level = "DEBUG"

logging.basicConfig(level=logging_level)
logging.info("Logging level set to '{0}'.".format(logging_level))

messages = [
    "Where are you? You're at my house and you should learn some manners!",
    "Who am I? Why I'm PapaGünzburg!",
    "If you must know, I am a scientist.  I don't know what forces brought you here.",
    "Nosy, aren't you. I deal in bots. Need a bot for a purpose, whatever purpose, I have that bot.",
    "How does a bot work? Wouldn't you like to know.",
    "Hmpff! Like you and I, bots can traverse the verse freely. It all comes down to having an\
    appropriate array of bi-carbon nanotubes so that the Vulkan Field regenerator maintains\
    singularity through the use of a yttrium-77 diffuser. There, satisfied?",
    "No one ever cares about my science :frowning:",
]

class PapaClient(discord.Client):
    def __init__(self):
        super().__init__()
        self._counter = 0

    async def on_message(self, message):
        if not message.author.bot and isinstance(message.channel, discord.TextChannel):
            expiration = datetime.datetime.utcnow() - datetime.timedelta(0, 30)
            deleted = await message.channel.purge(before=expiration)

            self._counter = (self._counter + 1) % len(messages)
            await message.channel.send(messages[self._counter])

    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.message.content == messages[5]:
            await user.send("Aw shucks, I didn't know you really cared!")
            await user.send("Here's the key, invite whoever you'd like!")
            for role in user.guild.roles:
                if role.name == "chum":
                    chum_role = role
            await user.edit(roles=[chum_role])

papa = PapaClient()
papa.run(config.token)
