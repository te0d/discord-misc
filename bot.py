import discord
import inflect
import logging
import re

from argparser import parser, subparsers
from player import Player

plu = inflect.engine()
shortcut_regex = re.compile(r"^;;\s*(?P<args>.*)", re.IGNORECASE)

PLAYERS = {
}

class ResourcefulClient(discord.Client):
    async def on_ready(self):
        logging.info("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        # Check for command
        match = shortcut_regex.match(message.content)
        if (not match):
            return

        logging.debug("Recognized command from {0.author}: {0.content}".format(message))

        # Parse arguments
        try:
            raw_args = parser.convert_arg_line_to_args(match.group("args"))
            args = parser.parse_args(raw_args)
        except ValueError as err:
            await message.channel.send(err)
            return

        # Perform action
        player = self.get_player(message.author)
        if (args.command is None):
            help_msg = "```\n{0}\n```".format(parser.format_help())
            await message.channel.send(help_msg)
        else:
            response = args.action(player, args)
            if (response):
                await message.channel.send(response)

    def get_player(self, user):
        username = str(user)
        if (not username in PLAYERS):
            logging.info("Adding new user: {0}".format(username))
            PLAYERS[username] = Player(user)

        return PLAYERS[username]

    def help(self, player, args):
        help_parser = subparsers.choices[args.topic] if args.topic else parser
        help_msg = "```\n{0}\n```".format(help_parser.format_help())
        return help_msg

    def list(self, player, args):
        output = ""
        items = player.inv.items
        if (len(items) == 0):
            output = "{0} doesn't have any stuff".format(player.display_name)
        else:
            output = "{0}'s stuff:\n```\n".format(player.display_name)
            for name in items:
                count = items[name].count
                output += "{:10.0f} {}\n".format(count, plu.plural(name, count))

            output += "```"

        return output

    def add(self, player, args):
        item = " ".join(args.item)
        player.inv.add(item, args.count)
        return None

    def drop(self, player, args):
        item = " ".join(args.item)
        player.inv.drop(item, args.count)
        return None

# Create discord client and hook-up sub-commands
client = ResourcefulClient()
subparsers.choices["help"].set_defaults(action=client.help)
subparsers.choices["list"].set_defaults(action=client.list)
subparsers.choices["add"].set_defaults(action=client.add)
subparsers.choices["drop"].set_defaults(action=client.drop)

client.run("Njk1NDY1NjQ5NjE0MzU2NTIw.XoamxQ.EKYprVdf7naBU1uS-Wcffxu12Ko")
