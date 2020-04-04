import discord
import inflect
import re

from argparser import parser

shortcutRegex = re.compile(r'^/res\b\s*(?P<args>.*)', re.IGNORECASE)
plu = inflect.engine()

STATE = {
}

class ResourcefulClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        match = shortcutRegex.match(message.content)
        if match:
            print('Recognized message from {0.author}: {0.content}'.format(message))

            fullArgs = match.group('args')
            try:
                args = parser.parse_args(match.group('args').split())
            except ValueError as err:
                await message.channel.send(err)
                return

            if (args.command is None):
                await message.channel.send(parser.print_help())
                return

            if (args.command == 'list' or args.command == 'l'):
                await message.channel.send(self.list(message.author))
            elif (args.command == 'add'or args.command == 'a'):
                item = ' '.join(args.item)
                item = plu.singular_noun(item) or item
                self.add(message.author, item, args.count)
            elif (args.command == 'drop' or args.command == 'd'):
                item = ' '.join(args.item)
                item = plu.singular_noun(item) or item
                self.drop(message.author, item, args.count)

    def list(self, user):
        username = str(user)
        if (not username in STATE or len(STATE[username].items()) == 0):
            return user.display_name + ' has no stuff.'

        output = user.display_name + '\'s stuff:\n```\n'
        for item, props in STATE[username].items():
            output += '{:10.0f}'.format(props['count']) + ' ' + plu.plural(item, props['count']) + '\n'

        output += '```'
        return output

    def add(self, user, item, count):
        username = str(user)
        item = plu.singular_noun(item) or item

        if (not username in STATE):
            STATE[username] = {}

        if (not item in  STATE[username]):
            STATE[username][item] = { 'count': 0 }

        if (count == None):
            count = 1

        STATE[username][item]['count'] += count

    def drop(self, user, item, count):
        username = str(user)
        if (count == None):
            count = 1

        if (username in STATE and item in STATE[username]):
            STATE[username][item]['count'] -= count
            if STATE[username][item]['count'] <= 0:
                del STATE[username][item]

client = ResourcefulClient()
client.run('Njk1NDY1NjQ5NjE0MzU2NTIw.XoamxQ.EKYprVdf7naBU1uS-Wcffxu12Ko')
