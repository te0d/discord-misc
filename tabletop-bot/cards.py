import random

class Tabletop:
    def __init__(self):
        self.decks = []
        self.hands = []

class CardDeck:
    def __init__(self, name, cardsDefinition, index):
        cards = []
        for cardDef in cardsDefinition['cards']:
            for n in range(cardDef['count']):
                card = Card(cardDef['name'], cardDef['description'], index)
                cards.append(card)

        random.shuffle(cards)

        self.name = name
        self.stock = cards          # fancy word I learned for undealt cards
        self.discard = []

    def deal(self, cardCount, playerCount):
        theDeal = [[] for pn in range(playerCount)]
        for cn in range(cardCount):
            for pn in range(playerCount):
                theDeal[pn].append(self.draw())

        return theDeal

    def draw(self):
        return self.stock.pop()

class Card:
    def __init__(self, name, description, deck_index):
        self.name = name
        self.description = description
        self.deck_index = deck_index

    def __repr__(self):
        return self.name

class Hand:
    """For our purpose, this is any collection of cards possessed by a player of the table;
    For instance, a rummy player would have 1 held hand and multiple "hands" shown for points.
    in hold-em, the table would have a hand shown of the community cards"""

    def __init__(self):
        self.cards = []
        self.private = True

    def play(self, cardIndex):
        return self.cards.pop(cardIndex)

    def __str__(self):
        output = ""
        for i in range(len(self.cards)):
            output += "{:2.0f}: {}\n".format(i, self.cards[i].name)

        return output
    def append(self, card):
        self.cards.append(card)
