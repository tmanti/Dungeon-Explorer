# Enemy class started Jan 17, 2019

import pygame
import dataTypes

enemyTypes = {}

class dropTable:
    def __init__(self, dropsList):
        self.dropsList = dropsList

class Enemy(pygame.sprite.Sprite):
    def __init__(self, stats, position, drops):
        super().__init__()

        self.stats = stats
        self.position = position
        self.tilePos = dataTypes.pos(self.position.x // 32, self.position.y // 32)
        self.chunkPos = dataTypes.pos(self.tilePos.x // 16, self.tilePos.y // 16)

        self.droptable = drops