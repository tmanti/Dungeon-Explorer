import item
import random
import pygame

FPS = 120
frames = FPS/8

chunkSize = 16

w,h = [800, 800]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#get game font
GAME_FONT_BUTTON = pygame.font.Font("8-bit.ttf", 27)
GAME_FONT = pygame.font.Font("8-bit.ttf", 30)
GAME_FONT_BIG = pygame.font.Font("8-bit.ttf", 40)
GAME_FONT_SMALL = pygame.font.Font("8-bit.ttf", 20)

GUI_FONT = pygame.font.Font("Pixel-Miners.otf", 30)
GUI_FONT_BIG = pygame.font.Font("Pixel-Miners.otf", 40)
GUI_FONT_SMALL = pygame.font.Font("Pixel-Miners.otf", 20)
GUI_FONT_BUTTON = pygame.font.Font("Pixel-Miners.otf", 27)

class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.__repr__ = self.__str__

    def return_Position(self):
        return {"x":self.x, "y":self.y}

    def __str__(self):
        return str(self.x)+ ":" + str(self.y)

class entityStats:
    def __init__(self, hp=0, mp=0, defen=0, spd=0, atk=0, dex=0, vit=0):
        self.health = hp
        self.defence = defen
        self.magic = mp
        self.speed = spd
        self.attack = atk
        self.dexterity = dex
        self.vitality = vit

    def return_entityStats(self):
        return {"hp":self.health, "mp":self.magic, "def": self.defence, "spd": self.speed, "atk": self.attack, "dex":self.dexterity, "vit": self.vitality}

class container:
    def __init__(self, size, contents=None):
        self.size = size
        if contents:
            self.contents = {}
            for x in range(self.size):
                self.contents[str(x)] = item.ItemStack(1, item.allItems[contents[str(x)]])
        else:
            self.contents={str(_):item.ItemStack(1, item.Nothing) for _ in range(self.size)}

    def return_Container(self):
        toReturn = self.contents
        for x in toReturn:
            toReturn[x] = toReturn[x].material.type
        return toReturn

class playerInventory:
    def __init__(self, weapon=item.ItemStack(1, item.Nothing), special=item.ItemStack(1, item.Nothing), armour=item.ItemStack(1, item.Nothing), ring=item.ItemStack(1, item.Nothing), container=container(30)):
        self.weapon = weapon
        self.special = special
        self.armour = armour
        self.ring = ring
        self.container = container

    def return_playerInventory(self):
        return {"weapon":self.weapon.material.type, "special":self.special.material.type, "armour":self.armour.material.type, "ring":self.ring.material.type, "container":self.container.return_Container()}

    def newWarriorInv(self):
        self.weapon = "Test"

class playerData:
    def __init__(self, position, inventory, stats, classType):
        self.position = position
        self.inventory = inventory
        self.stats = stats
        self.playerClass = classType

    def return_playerData(self):
        return {"pos":self.position.return_Position(), "inv":self.inventory.return_playerInventory(), "stats": self.stats.return_entityStats(), "class":self.playerClass.ClassType}

class chunkData:
    def __init__(self, pos, chunkData=None):
        self.chunkPos = pos
        self.chunkData = chunkData

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