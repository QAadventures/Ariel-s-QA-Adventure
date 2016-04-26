#superclass for items
class Item():
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

#subclass of items
class Coins(Item):
    def __init__(self, amt):
        self.amt = amt
        super(Coins, self).__init__(name="Hash Coin",
                         description="{} bucks worth of juicy round hash coins.".format(str(self.amt)),
                         value=self.amt)

    def add(self, amt):
        self.amt += amt
        self.description = "{0} bucks worth of shiny smelly hash coins.".format(str(self.amt))
        self.value = self.amt

#superclass for weapons
class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

        def __str__(self):
            return "{}\n=====\n{}Value: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)

#subclass1 for weapons
class Manual(Weapon):
    def __init__(self):
        super().__init__(name="Company policy manual",
                         description="The company policy manual, suitable for bludgeoning.",
                         value=0,
                         damage=5)

#subclass2 for weapons
class YasuTools(Weapon):
    def __init__(self):
        super().__init__(name="Yasu's stolen tools",
                         description="Sharp stolen tools from Yasu's cube. Somewhat more dangerous than the manual.",
                         value=10,
                         damage=10)

#subclass3 for weapons
class Emails(Weapon):
    def __init__(self):
        super().__init__(name="Passive-aggressive emails",
                        description="Passive-aggressive emails, with ALLL the executives cc'd. Certain to do damage",
                        value=15,
                        damage=15)
