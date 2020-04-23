import inflect

class Inventory:
    def __init__(self):
        self.items = {}
        self.inflect = inflect.engine()

    def add(self, name, count):
        name = self.inflect.singular_noun(name) or name
        if (not name in self.items):
            self.items[name] = InventoryItem(name, count)
        else:
            self.items[name].add(count)

    def drop(self, name, count):
        name = self.inflect.singular_noun(name) or name
        if (name in self.items):
            self.items[name].drop(count)
            if (self.items[name].count == 0):
                del(self.items[name])

class InventoryItem:
    def __init__(self, name, count):
        self.definition = None          # use ItemDefinition (via name) for stuff like calculating weight
        self._count = count

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if value < 0:
            value = 0

        self._count = value

    def add(self, count):
        self.count += count

    def drop(self, count):
        self.count -= count

class ItemDefinition:
    def __init__(self, name):
        self.name = name
