from inventory import Inventory

class Player:
    def __init__(self, user):
        self.name = str(user)
        self.display_name = user.display_name
        self.inv = Inventory()
