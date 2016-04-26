#superclass
class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

#subclasses
class Manager(Enemy):
    def __init__(self):
        super().__init__(name="Your manager", hp=10, damage=2)

class Exec(Enemy):
    def __init__(self):
        super().__init__(name="Angry executive", hp=30, damage=15)
        
class Programmer(Enemy):
    def __init__(self):
        super().__init__(name="Out of touch programmer", hp=20, damage=15)
