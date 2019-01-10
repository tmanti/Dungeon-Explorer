import item
import random

FPS = 120
frames = FPS / 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def return_Position(self):
        return {"x":self.x, "y":self.y}

class entityStats:
    def __init__(self, hp=0, mp=0, spd=0, atk=0, dex=0, vit=0):
        self.health = hp
        self.magic = mp
        self.speed = spd
        self.attack = atk
        self.dexterity = dex
        self.vitality = vit

    def return_entityStats(self):
        return {"hp":self.health, "mp":self.magic, "spd": self.speed, "atk": self.attack, "dex":self.dexterity, "vit": self.vitality}

class container:
    def __init__(self, size, contents=None):
        self.size = size
        if contents:
            self.contents = contents
        else:
            self.contents={_:item.Nothing for _ in range(self.size)}

    def return_Container(self):
        toReturn = self.contents
        for x in toReturn:
            toReturn[x] = toReturn[x].type
        return toReturn

class playerInventory:
    def __init__(self, weapon=item.Nothing, special=item.Nothing, armour=item.Nothing, ring=item.Nothing, container=container(30)):
        self.weapon = weapon
        self.special = special
        self.armour = armour
        self.ring = ring
        self.container = container

    def return_playerInventory(self):
        return {"weapon":self.weapon.type, "special":self.special.type, "armour":self.armour.type, "ring":self.ring.type, "container":self.container.return_Container()}

    def newWarriorInv(self):
        self.weapon = "Test"

class playerData:
    def __init__(self, position, inventory, stats, classType):
        self.position = position
        self.inventory = inventory
        self.stats = stats
        self.playerClass = classType

    def return_playerData(self):
        return {"pos":self.position.return_Position(), "inv":self.inventory.return_playerInventory(), "stats": self.stats.return_entityStats(), "class":self.playerClass.SlotType}

class worldData:
    def __init__(self, seed=random.randint(1, 100000)): #seed is used and stored for ease in the database, progression is used and stored in the database for the save as well (world events and other thigns)
        self.seed = seed

    def return_worldData(self):
        return {"seed":self.seed}

class saveData:
    def __init__(self, playerData, worldData):
        self.player = playerData
        self.world =  worldData

    def return_save(self):
        return [self.player.return_playerData(), self.world.return_worldData()]