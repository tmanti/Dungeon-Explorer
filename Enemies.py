# Enemy class started Jan 17, 2019

import pygame
import dataTypes
import random

all_enemies = pygame.sprite.Group()
def enemies():
    return all_enemies


class EnemyType:
    def __init__(self, type):
        if type == 'Grass':
            image = pygame.image.load('resources/Sprites/items/goblin.png')
            self.image = pygame.transform.scale(image, (image.get_height()*4, image.get_width()*4))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile, type):
        super().__init__()
        self.stats = dataTypes.entityStats(hp=20, mp=10, vit=random.randint(5, 17), dex=random.randint(5, 17), atk=random.randint(5, 17))
        self.tile = tile
        self.image = EnemyType(type).image
        all_enemies.add(self)

    def update(self, screen, playerPos):
        screen.blit(self.image, (self.tile.rect.x, self.tile.rect.y))
    def die(self):
        # calculate drops
        pass
