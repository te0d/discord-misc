from inventory import Inventory
from cards import Hand

class Player:
    def __init__(self, user):
        self.name = str(user)
        self.display_name = user.display_name

        self.inv = Inventory()

        self.decks = []
        self.hand = Hand()

    def draw(self, card):
        self.hand.append(card)
