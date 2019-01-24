# Enemy class started Jan 17, 2019

import pygame
import dataTypes
import xml.etree.ElementTree as ET
import item
import spritesheet
import random
import math
import copy

class dropTable:
    def __init__(self, dropsList):
        self.dropsList = dropsList

    def get_Drops(self):
        loot = []
        for x in self.dropsList:
            temp = random.randint(1, 100)
            if temp < x.chance:
                loot.append(item.ItemStack(random.randint(x.amount[0], x.amount[1]), x.Item))
        return loot

class dropCell:
    def __init__(self, itemId, chance, amount):
        self.Item = item.allItems[itemId]
        self.amount = [int(_) for _ in amount.split("-")]
        if len(self.amount) ==1:
            self.amount.append(self.amount[0])
        self.chance = chance

class Behavior:
    def __init__(self, type, distance=0, maxFollow=20):
        self.type = type
        self.distance = int(distance)*32
        self.maxFollow = maxFollow*32

class Bullet(pygame.sprite.Sprite):
    def __init__(self, projectileTexture, startPos, moveTo, rotation, bulletSpeed=1, toTravel=0, damage=0):
        super().__init__()
        self.position = dataTypes.pos(startPos.x, startPos.y)
        self.startPos = dataTypes.pos(self.position.x, self.position.y)
        self.image = projectileTexture
        self.moveTo = moveTo
        self.bulletSpeed = bulletSpeed*0.03
        self.distance = dataTypes.pos(self.moveTo.x - self.position.x, self.moveTo.y - self.position.y)
        self.toTravel = toTravel
        self.image = pygame.transform.rotate(self.image, rotation-45)

        self.damage = damage

        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def update(self, playerPos, *args):
        if math.sqrt((self.position.x - self.startPos.x)**2 + (self.position.y - self.startPos.y)**2) >= self.toTravel:
            self.kill()

        velo = [self.distance.x*self.bulletSpeed, self.distance.y*self.bulletSpeed]
        self.position.x +=velo[0]
        self.position.y +=velo[1]

        self.rect.x = self.position.x-playerPos.x
        self.rect.y = self.position.y-playerPos.y

class EnemyData:
    def __init__(self, group, type, name, stats, texture, projectile, drops, behavior):
        self.entityGroup = group
        self.type= type
        self.name = name

        self.stats = stats

        self.Texture = texture
        self.projectile = projectile

        self.behavior = behavior

        self.droptable = drops

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, stats, data):
        super().__init__()
        self.data = data

        self.stats = dataTypes.entityStats(hp=stats["hp"], defen=stats["def"], spd=stats["spd"],
                                           dex=stats["dex"])
        self.position = dataTypes.pos(x, y)

        self.damage = stats["atk"]
        if len(self.damage) == 1:
            self.damage.append(self.damage[0])

        self.canAttack = True
        self.wait = 0

        ss = spritesheet.spritesheet(self.data.Texture.fileLocation)
        self.image = ss.image_at(
            pygame.Rect(self.data.Texture.index[0], self.data.Texture.index[1], self.data.Texture.size, self.data.Texture.size),
            colorkey=dataTypes.WHITE)

        ss = spritesheet.spritesheet(self.data.projectile.fileLocation)
        self.projImage = ss.image_at((self.data.projectile.index[0], self.data.projectile.index[1], 8, 8),
                                     colorkey=dataTypes.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.tilePos = dataTypes.pos(self.position.x // 32, self.position.y // 32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // 16, self.tilePos.y // 16)

        self.projRange = 5

        self.bullets = pygame.sprite.Group()

    def update(self, playerPos, screen, *args):
        self.tilePos = dataTypes.pos(self.position.x // 32, self.position.y // 32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // dataTypes.chunkSize, self.tilePos.y // dataTypes.chunkSize)
        self.HpBar = pygame.Surface((50, 10))
        pygame.draw.rect(self.HpBar, dataTypes.RED, (0, 0, ((50 / allMobs[self.data.type].stats["hp"]) * self.stats.health), 10))

        velo = [0, 0]

        if self.data.behavior.type == "follow":
            direction = [playerPos.x+dataTypes.w//2>self.position.x, playerPos.y+dataTypes.h//2 > self.position.y]
            if ((playerPos.x+dataTypes.w//2-self.position.x)**2 + (playerPos.y+dataTypes.h//2-self.position.y)**2)**0.5 < self.data.behavior.maxFollow:
                if abs(playerPos.x+dataTypes.w//2-self.position.x) > self.data.behavior.distance:
                    if direction[0]:
                        velo[0]+=self.stats.speed
                    else:
                        velo[0]-=self.stats.speed
                elif (playerPos.y+dataTypes.h//2-self.data.behavior.distance < self.position.y < playerPos.y+dataTypes.h//2+self.data.behavior.distance):
                    if direction[0]:
                        velo[0]-=self.stats.speed
                    else:
                        velo[0]+=self.stats.speed

                if abs(playerPos.y+dataTypes.h//2-self.position.y) > self.data.behavior.distance:
                    if direction[1]:
                        velo[1]+=self.stats.speed
                    else:
                        velo[1]-=self.stats.speed
                elif (playerPos.x+dataTypes.w//2-self.data.behavior.distance < self.position.x < playerPos.x+dataTypes.w//2+self.data.behavior.distance):
                    if direction[1]:
                        velo[1]-=self.stats.speed
                    else:
                        velo[1]+=self.stats.speed

        if ((playerPos.x+dataTypes.w//2-self.position.x)**2 + (playerPos.y+dataTypes.h//2-self.position.y)**2)**0.5 < 5*32 and self.canAttack:
            self.Fire(playerPos)
            self.canAttack=False
            self.wait = pygame.time.get_ticks() + 3000

        if pygame.time.get_ticks() > self.wait:
            self.canAttack = True

        self.position.x += velo[0]
        self.position.y += velo[1]

        self.rect.x = self.position.x - playerPos.x
        self.rect.y = self.position.y - playerPos.y

        screen.blit(self.HpBar, (self.rect.x-10, self.rect.y+50))

    def Fire(self, playerPos):
        rel_x, rel_y = playerPos.x - self.rect.x , playerPos.y- self.rect.y
        angle = (180/math.pi) * -math.atan2(rel_y, rel_x)
        moveToPos = dataTypes.pos(self.projRange*math.cos(angle/55.47)+dataTypes.w//2, self.projRange*math.sin(-angle/55.47)+ dataTypes.h//2)
        moveToPos.x+=playerPos.x
        moveToPos.y += playerPos.y
        self.bullets.add(Bullet(self.projImage, dataTypes.pos(self.position.x, self.position.y), moveToPos, angle, toTravel=self.projRange*32, damage=random.randint(self.damage[0], self.damage[1])))

    def hit(self, damage):
        self.stats.health-=damage
        if self.stats.health <= 0:
            self.kill()
            return [True, self.data.droptable.get_Drops(), random.randint(1, 3)] #did kill - #drops - #exp gained
        else:
            return [False]



allMobs = {}
goblins = {}

def init():
    tree = ET.parse("resources/xml/enemies.xml")
    root = tree.getroot()
    for child in root:
        allMobs[child.get('type')] = EnemyData(
            child.find("Group").text,
            child.get("type"),
            child.get("id"),
            {
                "hp": int(child.find("stats").find("Hitpoints").text),
                "def": int(child.find("stats").find("Defence").text),
                "spd": int(child.find("stats").find("Speed").text),
                "atk": [int(_) for _ in child.find("stats").find("Attack").text.split("-")],
                "dex": int(child.find("stats").find("Dexterity").text)
            },
            item.spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "enemies"),
            item.spriteRef(child.find("ProjectileTexture").find("File").text, child.find("ProjectileTexture").find("Index").text, "enemies"),
            dropTable([dropCell(x.find("itemId").text, int(x.find("Chance").text), x.find("Amount").text) for x in child.find("DropTable").findall("DropCell")]),
            Behavior(child.find("Behavior").get("type"), distance=child.find("Behavior").get("distance"))
        )
        if child.find("Group").text == "Goblins":
            goblins[child.get('type')] = allMobs[child.get('type')]
        #elif child.find("")