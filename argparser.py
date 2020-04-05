import argparse

class BotArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()

    def error(self, message):
        raise ValueError(message)

parser = BotArgumentParser(prog=";;", description="loot bot", add_help=False)

subparsers = parser.add_subparsers(dest="command", help="sub-command help")

parser_help = subparsers.add_parser("help", aliases=["h"], add_help=False, help="print help")
parser_help.add_argument("topic",
                         type=str,
                         nargs="?",
                         help="name of subcommand")

parser_list = subparsers.add_parser("list", aliases=["l"], add_help=False, help="list possessions")

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
