import pygame
import dataTypes
import item
import pygame
import spritesheet

pos = dataTypes.pos

class warriorClass:
    def __init__(self):
        self.SlotType = 1
        self.projectileDistance = 4
        self.name = "Warrior"

    def setupClass(self, playerInv):
        playerInv.weapon =item.ItemStack(1,  item.allItems["0xa00"])

class mageClass:
    def __init__(self):
        self.SlotType = 2
        self.projectileDistance = 12
        self.name = "Mage"

    def setupClass(self, playerInv):
        playerInv.weapon = item.ItemStack(1, item.allItems["0xb00"])

class rangerClass:
    def __init__(self):
        self.SlotType = 3
        self.projectileDistance = 8
        self.name = "Ranger"

    def setupClass(self, playerInv):
        playerInv.weapon = item.ItemStack(1, item.allItems["0xc00"])

class player(pygame.sprite.Sprite):
    def __init__(self, setupData):
        super().__init__()
        self.position = setupData.position
        self.tilePos = dataTypes.pos(self.position.x//32, self.position.y//32)
        self.chunkPos = dataTypes.pos(self.tilePos.x//16, self.tilePos.y//16)
        self.inventory = setupData.inventory
        self.stats = setupData.stats

        self.playerClass = setupData.playerClass

        self.playerClass.setupClass(self.inventory)

        ss = spritesheet.spritesheet('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png')#get spritesheet reference
        self.playerIdle = [#list of player idle states
            ss.image_at((0, 8, 8, 8), colorkey=dataTypes.WHITE),#down
            ss.image_at((0, 0, 8, 8), colorkey=dataTypes.WHITE),#right
            ss.image_at((0, 24, 8, 8), colorkey=dataTypes.WHITE),#up
            ss.image_at((0, 16, 8, 8), colorkey=dataTypes.WHITE)#left
        ]
        self.playerWalk = [
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png', (8, 8, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#down
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png', (0, 0, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#right
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png', (8, 24, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#up
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + className[self.playerClass.SlotType].name + '.png', (0, 16, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames)#left
        ]

        self.playerAnim = self.playerIdle[0]
        self.lastFaced = 0

        self.rect = self.playerAnim.get_rect()
        self.rect.x = dataTypes.w/2
        self.rect.y = dataTypes.h/2

        self.attacking = False

    def update(self, screen, *args):
        #update position
        #draw
        self.tilePos = dataTypes.pos(self.position.x//32, self.position.y//32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // dataTypes.chunkSize, self.tilePos.y // dataTypes.chunkSize)
        
        keys = pygame.key.get_pressed()

        velocity = [0, 0]

        #0 - down, 1 - right, 2 - up, 3 - left

        if keys[pygame.K_w]:
            velocity[1] -= 1*self.stats.speed
            self.playerAnim = self.playerWalk[2].next()
            self.lastFaced = 2
        if keys[pygame.K_s]:
            velocity[1] += 1 * self.stats.speed
            self.playerAnim = self.playerWalk[0].next()
            self.lastFaced = 0
        if keys[pygame.K_a]:
            velocity[0] -= 1 * self.stats.speed
            self.playerAnim = self.playerWalk[3].next()
            self.lastFaced = 3
        if keys[pygame.K_d]:
            velocity[0] += 1 *self.stats.speed
            self.playerAnim = self.playerWalk[1].next()
            self.lastFaced = 1

        mousePressed = pygame.mouse.get_pressed()

        attacking = False

        if mousePressed[0] == 1:
            attacking =  True
        else:
            self.attacking = False
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        if self.attacking != attacking and attacking == True:
            pygame.time.set_timer(pygame.USEREVENT+1, 3000//self.stats.dexterity)
            self.attacking = True

        if self.attacking:
            #mousePos = pygame.mouse.get_pos()
            self.playerAnim = self.playerIdle[self.lastFaced]
        elif velocity == [0, 0]:
            self.playerAnim = self.playerIdle[self.lastFaced]

        self.position.x += velocity[0]
        self.position.y += velocity[1]

    def return_playerData(self):
        return dataTypes.playerData(self.position, self.inventory, self.stats, self.playerClass)

def generateNewPlayerData(playerClass):
    return dataTypes.playerData(pos(0, 0), dataTypes.playerInventory, dataTypes.entityStats(hp=20, mp=20, defen=5, spd=3, atk=5, dex=5, vit=5), playerClass)

testPlayerData = dataTypes.playerData(pos(0, 0), dataTypes.playerInventory(), dataTypes.entityStats(hp=20, mp=20, defen=5, spd=3, atk=5, dex=5, vit=5), warriorClass())
className = {1:warriorClass(), 2:mageClass(), 3:rangerClass()}