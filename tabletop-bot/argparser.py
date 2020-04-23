import argparse

class BotArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()

    def error(self, message):
        raise ValueError(message)

parser = BotArgumentParser(prog="%", description="loot bot", add_help=False)

subparsers = parser.add_subparsers(dest="command", help="sub-command help")

parser_help = subparsers.add_parser("help", aliases=["h"], add_help=False, help="print help")
parser_help.add_argument("topic",
                         type=str,
                         nargs="?",
                         help="name of subcommand")

## Inventory ##

parser_inv = subparsers.add_parser("inv", aliases=["i"], add_help=False, help="list possessions")

parser_add = subparsers.add_parser("add", aliases=["a"], add_help=False, help="add possessions")
parser_add.add_argument("-c", "--count",
                    type=int,
                    default=1,
                    help="amount of items")
parser_add.add_argument("item",
                    type=str,
                    nargs="+",
                    help="name of item")

parser_drop = subparsers.add_parser("drop", aliases=["d"], add_help=False, help="remove possessions")
parser_drop.add_argument("-c", "--count",
                    type=int,
                    default=1,
                    help="amount of items")
parser_drop.add_argument("item",
                    type=str,
                    nargs="+",
                    help="name of item")

## Cards ##

parser_cards = subparsers.add_parser("cards", aliases=["c"], add_help=False, help="put decks into play and get info")
parser_cards_group = parser_cards.add_mutually_exclusive_group()
parser_cards_group.add_argument("-i", "--init",
                          metavar='DECKNAME',
                          type=str,
                          help="name of deck to put into play")
parser_cards_group.add_argument("-d", "--deck",
                          metavar='DECKINDEX',
                          type=int,
                          help="display info about deck on tabletop")

parser_draw = subparsers.add_parser("draw", add_help=False, help="draw a card to your hand")
parser_draw.add_argument("-d", "--deck",
                         metavar='DECKINDEX',
                         type=int,
                         help="index of deck in play to draw a card from")

parser_hand = subparsers.add_parser("hand", add_help=False, help="look at and play your cards")
parser_hand.add_argument("-p", "--play",
                         metavar='CARDINDEX',
                         type=int,
                         help="index of hand card to play to table")

## Dice ##

parser_roll = subparsers.add_parser("roll", aliases=["r"], add_help=False, help="roll some dice")
parser_roll.add_argument("dice",
                         type=str,
                         help="dice to roll like, e.g. 3d6")
