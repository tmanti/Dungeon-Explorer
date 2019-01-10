import pygame
import dataTypes

pos = dataTypes.pos

# - - BORROWED CODE - - https://www.pygame.org/wiki/Spritesheet - -
class SpriteStripAnim(object):
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim

        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.

        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.

        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        x,y = image.get_size()
        image = pygame.transform.scale(image, (x*4, y*4))
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey)
# - - END BORROWED CODE - -

class warriorClass:
    def __init__(self):
        self.SlotType = 1
        self.projectileDistance = 4
        self.name = "Warrior"

class mageClass:
    def __init__(self):
        self.SlotType = 2
        self.projectileDistance = 12
        self.name = "Mage"

class rangerClass:
    def __init__(self):
        self.SlotType = 3
        self.projectileDistance = 8
        self.name = "Ranger"

class player:
    def __init__(self, setupData):
        self.position = setupData.position
        self.inventory = setupData.inventory
        self.stats = setupData.stats

        self.playerClass = setupData.playerClass

        ss = spritesheet('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png')#get spritesheet reference
        self.playerIdle = [#list of player idle states
            ss.image_at((0, 8, 8, 8), colorkey=dataTypes.WHITE),#down
            ss.image_at((0, 0, 8, 8), colorkey=dataTypes.WHITE),#right
            ss.image_at((0, 24, 8, 8), colorkey=dataTypes.WHITE),#up
            ss.image_at((0, 16, 8, 8), colorkey=dataTypes.WHITE)#left
        ]
        self.playerWalk = [
            SpriteStripAnim('sprites/playerSpriteSheet.png', (8, 8, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#down
            SpriteStripAnim('sprites/playerSpriteSheet.png', (0, 0, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#right
            SpriteStripAnim('sprites/playerSpriteSheet.png', (8, 24, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#up
            SpriteStripAnim('sprites/playerSpriteSheet.png', (0, 16, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames)#left
        ]

    def return_playerData(self):
        return dataTypes.playerData(self.position, self.inventory, self.stats, self.playerClass)


newPlayerData = dataTypes.playerData(pos(0, 0), dataTypes.playerInventory(), dataTypes.entityStats(hp=20, mp=20, spd=5, atk=5, dex=5, vit=5), warriorClass())
className = {1:warriorClass, 2:mageClass, 3:rangerClass}