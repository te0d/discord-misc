import argparse

class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

parser = ErrorRaisingArgumentParser(description='loot bot', add_help=False)
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

parser_list = subparsers.add_parser('list', aliases=['l'], help='list possessions')

parser_add = subparsers.add_parser('add', aliases=['a'], add_help=False, help='add possessions')
parser_add.add_argument('-count',
                    type=int,
                    default=1,
                    help='amount of items')
parser_add.add_argument('item',
                    metavar='I',
                    type=str,
                    nargs='+',
                    help='name of item')

parser_drop = subparsers.add_parser('drop', aliases=['d'], add_help=False, help='remove possessions')
parser_drop.add_argument('-count',
                    type=int,
                    default=1,
                    help='amount of items')
parser_drop.add_argument('item',
                    metavar='I',
                    type=str,
                    nargs='+',
                    help='name of item')

# args = parser.parse_args()
# print(args)
