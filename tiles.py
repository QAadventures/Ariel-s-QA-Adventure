import items, enemies, actions, world

#abstract base class bc no instances of this
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = "????????"

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, the_player):
        raise NotImplementedError()

#default tile behavior
    def adjacent_moves(self): #returns all move actions for adjacent tiles & determines which moves are possible
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self): #returns all available actions in the room
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.ViewMap())

        return moves


#subclasses
#starting room subclass
class StartingRoom(MapTile):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.id = "START"
    
    def intro_text(self):
        return """\n\n\nYou find yourself in your cubicle, hearing screams and shouts around you.
You can make out four paths, each equally shitty-looking.
Where in the office maze will you end up today??
Follow the white rabbit...
You start out with 15 bucks worth of hash coins to bargain with.
\n\nDISCLAIMER FOR EVERYONE: This game is slightly crass & uses strong language.
Play at your own risk!!
\n\nDISCLAIMER FOR BOSSES: The hash coin thing is a joke from Trailer Park Boys!!
If you've never watched that show, you should. All seasons are on Netflix!
\nAlso I DO actually like my job! Just saying!
        """

    def modify_player(self, the_player):
        #room has no action on player
        pass

#the 3 major room subclasses - not in program directly, only subclasses of these can be interacted with
#loot room subclass
class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x,y)

    def add_loot(self, the_player):
        if isinstance(self.item, items.Coins):
            the_player.add_gold(self.item.amt)
        else:
            the_player.inventory.append(self.item)

        self.item = None

    def modify_player(self, the_player): 
        if self.item:
            self.add_loot(the_player) 

#enemy room subclass
class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("The enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

#empty room subclass
class EmptyPath(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = "Empty office path"
    
    def intro_text(self):
        return """
    Another boring part of the office - nothing exciting here. You must go on!
        """

    def modify_player(self, the_player):
        #room has no action on player
        pass

#additional types of loot rooms & enemy rooms - user interacts with these directly
#Nick's cubicle room, subclass of lootroom, Yasu's tools are located here
class NicksCube(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.YasuTools())
        self.id = "Nick's Cubicle"

    def intro_text(self):
        if self.item:
            return """
    You notice something in Nick's cube alongside the mouse battery graveyard!
    It's Yasu's net building tools! You steal them!
    These are sure to do some damage!!
            """

        else:
            return """
    You already took Yasu's net building tools that were here. Make sure
    you keep being sneaky so nobody notices they're missing!!
    Just like how the scissors are always missing from the 
            """

#IT guy's cubicle, find passive aggressive emails ehre
class ITCube(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Emails())
        self.id = "IT guy's cubicle"

    def intro_text(self):
        if self.item:
            return """
    You wander into the IT guy's cubicle...
    You find a bunch of passive-aggressive emails, with all the execs cc'd!!
    You could use these as a weapon against enemies!!
    You copy+paste them away for later...
            """
        else:
            return """
    You already found the passive-aggressive emails that were once here.
    You look around for more, but dont' find anything new.
    Maybe check your own inbox instead?
    But that game feature has not been implemented yet.... stupid code monkeys.
            """

#QA friend's cubicle, find policy mnual here
class ManualCube(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Manual())
        self.id = "Coworker's cubicle"

    def intro_text(self):
        if self.item:
            return """
    You wander into your QA friend's cubicle!!
    You find a copy of the company policy manual!!
    It could be used as a weapon!!
    Not a very effective one though, since nobody reads it...
            """

        else:
            return """
    You already grabbed the company policy manual that was once here.
    Who on earth would want two copies anyway???
            """

#Find coins room 1
class FindCoinsRoom(LootRoom):
    def __init__(self, x,y):
        super().__init__(x, y, items.Coins(5))
        self.id = "Hash coins!!"

    def intro_text(self):
        if self.item:
            return """
    Somebody dropped a valuable hash coin!! You pick that shit up!!
    Looks to be worth about 5 bucks.
        """

        else:
            return"""
    Looks like you already got the hash coin that was in here.
    You look around the area like a fiend for a minute, but ultimately
    you can't find anything new.
            """

#enemy room with angry executive
class ExecRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Exec())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
    An angry executive is blocking your path!
    You must fight to prove you're not a total dumbass!!
            """
        else:
            return """
    The angry executive that was here has been pacified.... FOR NOW!!!
            """

#enemy room with out of touch programmer
class ProgrammerRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Programmer())
        self.id = "Out of touch programmer"

    def intro_text(self):
        if self.enemy.is_alive():
            return """
    An out of touch programmer is blocking your path!!!
    You must fight to get the needed SRS info from them!!!
            """
        else:
            return """
    You defeated the out of touch programmer who was once here.
    You remember your sweet victory and enjoy the reverie....
    Then you snap back to reality and realize that you're still
    just a little piss-ant tester at this place.
    The harsh realizty creeps back in and you're forced to move on.
    Go forward, great warrior!!!
            """

# figure out how to print this upon enemy defeat
#            return """
#    Somehow, you manage to get the needed information out of the programmer.\n
#    Great job!!\n
#    Now please write a report on how you accomplished this feat and distribute
#    it to the QA team ASAP, because we need to know.
#            """

#enemy room with manager
class ManagerRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Manager())
        self.id = "Your boss's office"

    def intro_text(self):
        if self.enemy.is_alive():
            return """
    You run into your manager and he starts making small talk!!
    OH NO!!!!\n
        \nAs you stare at him, his face warps around and he turns into a giant lizard....
    You must fight to get past him!!
            """
        else:
            return """
    You slowly peek around the corner...
    Your manager isn't back in his office yet. You sneak past!!
            """

#TO DO: if/when this boss's health goes to 0, then user gets this message
#    He finally stops his diarrhea of the mouth and lets you pass!!
#    Thank goodness!
#    Maybe you need a beer or something to relax after that train wreck.


#leave office room - going here makes you win
class LeaveOfficeRoom(MapTile):
    def intro_text(self):
        return """
    You see a bright light ahead... it's sunlight!!
    You've made it out of the cave-like office!

    Victory is yours!!! Until tomorrow...
        """

    def modify_player(self, player):
        player.victory = True
