import pygame
import Player
import db
import dataTypes
import item
import world
import json

# TODO LIST - make someone say mada mada
#for miller
# TODO LIST - hand_Okay
#for daniel

p = pygame
p.init()

dbInt = db.DBInterface()

pos = dataTypes.pos

display = p.display
clock = p.time.Clock()

try:
    GAME_FONT = pygame.font.Font("8-bit.ttf", 27)
except:
    GAME_FONT = pygame.font.SysFont("Arial", 27)

save = dbInt.save

def GenerateNewSave(playerName):
    player = Player.newPlayerData
    worldData = dataTypes.worldData()

    saveData = dataTypes.saveData(player, worldData).return_save()
    print(saveData)
    dbInt.newSave(playerName, json.dumps(saveData))

def loadSave(saveName):
    save = dbInt.checkSave(saveName)
    return ParseSaveData(json.loads(save.userdata))

def ParseSaveData(saveData):
    print(saveData)
    player = dataTypes.playerData(
        pos(saveData[0]['pos']['x'], saveData[0]['pos']['y']),
        dataTypes.playerInventory(weapon=saveData[0]['inv']['weapon'], special=saveData[0]['inv']['special'], armour=saveData[0]['inv']['armour'], ring=saveData[0]['inv']['ring'], container=dataTypes.container(30, saveData[0]['inv']['container'])),
        dataTypes.entityStats(hp=saveData[0]['stats']['hp'], mp=saveData[0]['stats']['mp'], spd=saveData[0]['stats']['spd'], atk=saveData[0]['stats']['atk'], dex=saveData[0]['stats']['dex'], vit=saveData[0]['stats']['vit']),
        Player.className[saveData[0]['class']]()
    )
    worldData = dataTypes.worldData(saveData[1]['seed'])

    return dataTypes.saveData(player, worldData)

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, action=None):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.action = action

    #def press(self):


class Client:
    #define constants
    run = True

    def __init__(self):
        #initialize pygame and the screen
        self.screen = p.display.set_mode((800, 800))#, pygame.FULLSCREEN)
        p.display.set_caption("Generic RPG")

        self.state = 1

        self.states = {"1": self.main_menu}

        item.init()

    def run(self):
        #main game loop
        while self.run:
            for e in p.event.get():#event queue
                if e.type == p.QUIT:
                    self.run = False
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        self.run = False

            self.states[str(self.state)]()

        #once while loop broken
        p.quit()
        return

    def main_menu(self):
        print("Menu")

#declaring game client
gameClient = Client()
gameClient.run()