import pygame
import dataTypes
import item
import pygame
import spritesheet
import math
import random

pos = dataTypes.pos

class warriorClass:
    name = "Warrior"
    ClassType = 1
    slotTypes = [1,2,3]
    projectileDistance = 4 *32

    def setupClass(self, playerInv):
        playerInv.weapon =item.ItemStack(1,  item.allItems["0xa00"])
        #moresetup

        return playerInv

class mageClass:
    name = "Mage"
    ClassType = 2
    slotTypes = [4,5,6]
    projectileDistance = 12 *32

    def setupClass(self, playerInv):
        playerInv.weapon = item.ItemStack(1, item.allItems["0xb00"])
        # moresetup

        return playerInv

class rangerClass:
    name = "Ranger"
    ClassType = 3
    slotTypes = [7,8,9]
    projectileDistance = 8 *32

    def setupClass(self, playerInv):
        playerInv.weapon = item.ItemStack(1, item.allItems["0xc00"])
        # moresetup

        return playerInv

class Bullet(pygame.sprite.Sprite):
    def __init__(self, projectileTexture, start, moveTo, rotation, Damage, bulletSpeed=1, toTravel=0):
        super().__init__()
        self.position = dataTypes.pos(start.x, start.y)
        self.startPos = dataTypes.pos(self.position.x, self.position.y)
        self.image = projectileTexture
        self.moveTo = moveTo
        self.bulletSpeed = bulletSpeed*0.03
        self.distance = dataTypes.pos(self.moveTo.x - self.position.x, self.moveTo.y - self.position.y)
        self.toTravel = toTravel

        self.damage = Damage

        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.image = pygame.transform.rotate(self.image, rotation-45)

    def update(self, playerPos, *args):
        if math.sqrt((self.position.x - self.startPos.x)**2 + (self.position.y - self.startPos.y)**2) >= self.toTravel:
            self.kill()

        velo = [self.distance.x*self.bulletSpeed, self.distance.y*self.bulletSpeed]
        self.position.x +=velo[0]
        self.position.y +=velo[1]

        self.rect.x = self.position.x - playerPos.x
        self.rect.y = self.position.y - playerPos.y

class player(pygame.sprite.Sprite):
    def __init__(self, setupData):
        super().__init__()
        self.position = setupData.position
        self.tilePos = dataTypes.pos(self.position.x//32, self.position.y//32)
        self.chunkPos = dataTypes.pos(self.tilePos.x//16, self.tilePos.y//16)
        self.inventory = setupData.inventory
        self.stats = setupData.stats

        self.currentHp = self.stats.health
        self.currentMp = self.stats.magic

        self.bullets = pygame.sprite.Group()

        self.level = setupData.level

        self.drawOffset = 0

        self.playerClass = setupData.playerClass

        self.inventory = self.playerClass.setupClass(self.inventory)

        ss = spritesheet.spritesheet('resources/Sprites/player/' + self.playerClass.name + '.png')#get spritesheet reference
        self.playerIdle = [#list of player idle states
            ss.image_at((0, 8, 8, 8), colorkey=dataTypes.WHITE),#down
            ss.image_at((0, 0, 8, 8), colorkey=dataTypes.WHITE),#right
            ss.image_at((0, 24, 8, 8), colorkey=dataTypes.WHITE),#up
            ss.image_at((0, 16, 8, 8), colorkey=dataTypes.WHITE)#left
        ]
        self.playerWalk = [
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + '.png', (8, 8, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#down
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + '.png', (0, 0, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#right
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + '.png', (8, 24, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames),#up
            spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + '.png', (0, 16, 8, 8), 2, dataTypes.WHITE, True, dataTypes.frames)#left
        ]

        if self.playerClass.name == warriorClass.name:
            self.playerAttack = [
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png", (0, 8, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True, frames=dataTypes.frames),#down
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png", (0, 0, 0, 0), 2, colorkey=dataTypes.WHITE, loop=True, frames=dataTypes.frames, images=[(0,0,8,8), (8,0,12,8)]),#right
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png", (0, 16, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True, frames=dataTypes.frames),#up
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png", (0, 0, 0, 0), 2, colorkey=dataTypes.WHITE, loop=True, frames=dataTypes.frames, images=[(0,24,12,8), (12,24,8,8)]),#left
            ]
        elif self.playerClass.name == mageClass.name:
            self.playerAttack = [
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 8, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # down
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 0, 0, 0), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames, images=[(0, 0, 8, 8), (8, 0, 11, 8)]),  # right
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 16, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # up
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 0, 0, 0), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames, images=[(0, 24, 11, 8), (11, 24, 8, 8)]),  # left
            ]
        elif self.playerClass.name == rangerClass.name:
            self.playerAttack = [
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 8, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # down
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 0, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # right
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 16, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # up
                spritesheet.SpriteStripAnim('resources/Sprites/player/' + self.playerClass.name + "Attacking.png",
                                            (0, 24, 8, 8), 2, colorkey=dataTypes.WHITE, loop=True,
                                            frames=dataTypes.frames),  # left
            ]

        self.playerAnim = self.playerIdle[0]
        self.lastFaced = 0

        self.rect = self.playerAnim.get_rect()
        self.rect.x = dataTypes.w//2-16
        self.rect.y = dataTypes.h//2-16

        self.attacking = False

    def update(self, *args):
        #update position
        #draw
        self.tilePos = dataTypes.pos(self.position.x//32, self.position.y//32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // dataTypes.chunkSize, self.tilePos.y // dataTypes.chunkSize)
        self.drawOffset = 0
        self.AttackingToggled = False

        keys = pygame.key.get_pressed()

        velocity = [0, 0]

        #0 - down, 1 - right, 2 - up, 3 - left

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            velocity[1] -= 1*self.stats.speed
            self.playerAnim = self.playerWalk[2].next()
            self.lastFaced = 2
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            velocity[1] += 1 * self.stats.speed
            self.playerAnim = self.playerWalk[0].next()
            self.lastFaced = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            velocity[0] -= 1 * self.stats.speed
            self.playerAnim = self.playerWalk[3].next()
            self.lastFaced = 3
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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

        if self.attacking != attacking and attacking == True and self.inventory.weapon.material.SlotType == str(self.playerClass.slotTypes[0]):
            pygame.time.set_timer(pygame.USEREVENT+1, 2500//(self.stats.dexterity+self.inventory.weapon.material.rateOfFire))
            self.attacking = True

        if self.attacking or self.AttackingToggled:
            #code from https://gamedev.stackexchange.com/a/134090
            mX, mY = pygame.mouse.get_pos()
            rel_x, rel_y = mX - dataTypes.w//2, mY - dataTypes.h//2
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            #end borrowed code (didnt want to remember math lol)

            if -45 <= angle and angle <= 45:
                self.lastFaced = 1
            elif 45 <= angle and angle <= 135:
                self.lastFaced = 2
            elif angle >= 135 or angle <= -135:
                self.lastFaced = 3
            elif -45 >= angle and angle >= -135:
                self.lastFaced = 0
            self.playerAnim = self.playerAttack[self.lastFaced].next()
            if self.playerAnim == self.playerAttack[3].images[0]:
                if self.playerClass.name == "Warrior":
                    self.drawOffset = -16
                elif self.playerClass.name == "Mage":
                    self.drawOffset = -12

        elif velocity == [0, 0]:
            self.playerAnim = self.playerIdle[self.lastFaced]

        self.position.x += velocity[0]
        self.position.y += velocity[1]

        self.currentHp += self.stats.vitality/2000

    def return_playerData(self):
        return dataTypes.playerData(self.position, self.inventory, self.stats, self.playerClass, self.level)

    def Fire(self, mousePos):
        rel_x, rel_y = mousePos[0] - dataTypes.w // 2, mousePos[1] - dataTypes.h // 2
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        moveToPos = dataTypes.pos(self.playerClass.projectileDistance * math.cos(angle / 55.47) + dataTypes.w // 2, self.playerClass.projectileDistance * math.sin(-angle / 55.47) + dataTypes.h // 2)
        moveToPos.x += self.position.x
        moveToPos.y += self.position.y
        startPos = dataTypes.pos(self.position.x+dataTypes.w//2, self.position.y+dataTypes.h//2)
        self.bullets.add(Bullet(self.inventory.weapon.material.projectileImage, startPos, moveToPos, angle, random.randint(self.inventory.weapon.material.damage[0], self.inventory.weapon.material.damage[1]), toTravel=self.playerClass.projectileDistance))

    def hit(self, damage):
        print("took " + str(damage))
        self.currentHp-=damage
        if self.currentHp <= 0:
            return True
        else:
            return False


def generateNewPlayerData(playerClass):
    return dataTypes.playerData(pos(0, 0), dataTypes.playerInventory(), dataTypes.entityStats(hp=40, mp=20, defen=5, spd=3, atk=5, dex=5, vit=5), playerClass(), dataTypes.Level(1, 0))

#testPlayerData = dataTypes.playerData(pos(0, 0), dataTypes.playerInventory(), dataTypes.entityStats(hp=40, mp=20, defen=5, spd=3, atk=5, dex=5, vit=5), warriorClass(), dataTypes.Level(1, 0))
className = {1:warriorClass(), 2:mageClass(), 3:rangerClass()}