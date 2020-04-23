import discord
import inflect
import logging
import random
import re

from argparser import parser, subparsers
from player import Player
from cards import CardDeck, Tabletop
from output import Output

import codex.catan
import codex.standard

plu = inflect.engine()
shortcut_regex = re.compile(r"^%\s*(?P<args>.*)", re.IGNORECASE)
dice_roll_regex = re.compile(r"^(?P<count>\d*)d(?P<sides>\d+)$", re.IGNORECASE)

TABLETOP = Tabletop()
PLAYERS = {
}
DECKS = {
    "catan_development": codex.catan.developmentDefinition,
    "standard": codex.standard.definition,
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
            output = args.action(player, args)
            if (output and output.private):
                await message.author.send(output.message)
            elif (output):
                await message.channel.send(output.message)

    def get_player(self, user):
        username = str(user)
        if (not username in PLAYERS):
            logging.info("Adding new user: {0}".format(username))
            PLAYERS[username] = Player(user)

        return PLAYERS[username]

    def help(self, player, args):
        help_parser = subparsers.choices[args.topic] if args.topic else parser
        help_msg = "```\n{0}\n```".format(help_parser.format_help())
        return Output(False, help_msg)

    def inv(self, player, args):
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

        return Output(False, output)

    def add(self, player, args):
        item = " ".join(args.item)
        player.inv.add(item, args.count)
        return None

    def drop(self, player, args):
        item = " ".join(args.item)
        player.inv.drop(item, args.count)
        return None

    def cards(self, player, args):
        if (args.init):
            output = self.cards_init(player, args)
        else:
            output = self.cards_list(player, args)

        return output

    def cards_init(self, player, args):
        deck_def = DECKS[args.init]
        index = len(TABLETOP.decks)
        deck = CardDeck(deck_def["name"], deck_def, index)
        TABLETOP.decks.append(deck)

    def cards_list(self, player, args):
        if (args.deck is not None):
            deck = TABLETOP.decks[args.deck]
            output = "```\n{0}: '{1}'\n   {2} stock, {3} discard\n```".format(args.deck, deck.name, len(deck.stock), len(deck.discard))
        else:
            output = "```\nAvailable Decks:\n"
            for name in DECKS:
                output += "* {}\n".format(name)

            output += "\nDecks In Play:\n"
            for n in range(len(TABLETOP.decks)):
                deck = TABLETOP.decks[n]
                output += "[{0}] {1}\n".format(n, deck.name)

            output += "```"

        return Output(False, output)

    def draw(self, player, args):
        if (args.deck is not None):
            deck = TABLETOP.decks[args.deck]
        else:
            deck = TABLETOP.decks[0]

        player.draw(deck.draw())

    def hand(self, player, args):
        if (args.play is not None):
            output = self.hand_play(player, args)
        else:
            output = self.hand_list(player, args)

        return output

    def hand_list(self, player, args):
        if (len(player.hand.cards) == 0):
            output = "You don't have any cards."
        else:
            output = "```\n{0}\n```".format(str(player.hand))

        return Output(True, output)

    def hand_play(self, player, args):
        card = player.hand.play(args.play)
        targetDeck = TABLETOP.decks[card.deck_index]
        targetDeck.discard.append(card)
        output = "{0} played {1}! *({2})*".format(player.display_name, card, card.description)
        return Output(False, output)

    def roll(self, player, args):
        output = "```\n"
        dice = args.dice
        match = dice_roll_regex.match(dice)
        output += "{0}:\n".format(dice)
        count = int(match.group("count")) if match.group("count") else 1
        sides = int(match.group("sides"))
        if (count > 100):
            return Output(False, "Sorry, I am unable to roll so many explicable dice.")
        elif (sides > 1000000000000):
            return Output(False, "Sorry, I have not dice with so many luscious sides.")

        rolls = []
        for n in range(count):
            roll = "[{}]".format(random.randrange(sides)+1) # how efficient
            rolls.append(roll)

        output += " ".join(rolls) + "\n```"

        return Output(False, output)


# Create discord client and hook-up sub-commands
client = ResourcefulClient()
subparsers.choices["help"].set_defaults(action=client.help)

subparsers.choices["inv"].set_defaults(action=client.inv)
subparsers.choices["add"].set_defaults(action=client.add)
subparsers.choices["drop"].set_defaults(action=client.drop)

subparsers.choices["cards"].set_defaults(action=client.cards)
subparsers.choices["draw"].set_defaults(action=client.draw)
subparsers.choices["hand"].set_defaults(action=client.hand)

subparsers.choices["roll"].set_defaults(action=client.roll)

client.run("Njk1NDY1NjQ5NjE0MzU2NTIw.XoamxQ.EKYprVdf7naBU1uS-Wcffxu12Ko")
