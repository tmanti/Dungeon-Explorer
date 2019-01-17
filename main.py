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

#init pygame
p = pygame
p.init()

#create a database interface
dbInt = db.DBInterface()

#another shortcut
pos = dataTypes.pos

#easy acces to display and clock
display = p.display
clock = p.time.Clock()

#get game font
try:
    GAME_FONT = pygame.font.Font("8-bit.ttf", 27)
except:
    GAME_FONT = pygame.font.SysFont("Arial", 27)

#reference to the save method
save = dbInt.save

#DATA BASE METHODS
#generate new save (compiles all information then writes to db)
def GenerateNewSave(playerName):
    player = Player.newPlayerData
    worldData = dataTypes.worldData()

    saveData = dataTypes.saveData(player, worldData).return_save()
    print(saveData)
    dbInt.newSave(playerName, json.dumps(saveData))

#loads a save then return the parsed save data
def loadSave(saveName):
    save = dbInt.checkSave(saveName)
    return ParseSaveData(json.loads(save.userdata))

#parses the save data and returns it as a saveData object for easy use
def ParseSaveData(saveData):
    print(saveData)
    player = dataTypes.playerData(
        pos(saveData[0]['pos']['x'], saveData[0]['pos']['y']),
        dataTypes.playerInventory(weapon=item.ItemStack(1, item.allItems[saveData[0]['inv']['weapon']]), special=item.ItemStack(1, item.allItems[saveData[0]['inv']['special']]), armour=item.ItemStack(1, item.allItems[saveData[0]['inv']['armour']]), ring=item.ItemStack(1, item.allItems[saveData[0]['inv']['ring']]), container=dataTypes.container(30, saveData[0]['inv']['container'])),
        dataTypes.entityStats(hp=saveData[0]['stats']['hp'], mp=saveData[0]['stats']['mp'], spd=saveData[0]['stats']['spd'], atk=saveData[0]['stats']['atk'], dex=saveData[0]['stats']['dex'], vit=saveData[0]['stats']['vit']),
        Player.className[saveData[0]['class']]
    )
    worldData = dataTypes.worldData(saveData[1]['seed'])

    return dataTypes.saveData(player, worldData)

#button object
#for reuse of easy buttoning
class button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, action=None):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.press = action

    def press(self):
        pass

class loadButton(button):
    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h, text, action=lambda x: gameClient.Load(text))

#main client object
class Client:
    #define constants
    run = True

    def __init__(self):
        #initialize pygame and the screen
        self.screen = p.display.set_mode((800, 800))#, pygame.FULLSCREEN)
        p.display.set_caption("Generic RPG")

        self.state = 2

        self.states = {1: self.main_menu, 2:self.game}

        #initialize items
        item.init()

        self.Load("tmanti")

        #genned Chunks dict to easily store all genned chunks for easy reuse
        self.gennedChunks = {}


    def run(self):
        #main game loop
        while self.run:
            for e in p.event.get():#event queue
                print(e)
                if e.type == p.QUIT:
                    self.run = False
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        self.run = False

            clock.tick(dataTypes.FPS)

            self.states[self.state]()

        #once while loop broken
        p.quit()
        return

    def main_menu(self):
        print("Menu")

    def game(self):
        #allChunks = [_.split(":") for _ in self.gennedChunks.keys()]
        #allChunks = [[int(allChunks[x][0]), int(allChunks[x][1])] for x in range(len(allChunks))]
        loadedChunks = []

        self.screen.fill(dataTypes.BLACK)

        self.Player.update(self.screen)

        toGen = dataTypes.pos(self.Player.chunkPos.x-1, self.Player.chunkPos.y-1)
        genTemp = dataTypes.pos(toGen.x, toGen.y)

        for y in range(3):
            genTemp.y = toGen.y+y
            genTemp.x = toGen.x
            for x in range(3):
                genTemp.x = toGen.x+x
                if str(genTemp) not in self.gennedChunks.keys():
                    self.gennedChunks[str(genTemp)] = world.Chunk(dataTypes.chunkData(genTemp))
                    self.gennedChunks[str(genTemp)].genChunk(self.World.genNoiseMap(self.gennedChunks[str(genTemp)].tilePos))
                loadedChunks.append(self.gennedChunks[str(genTemp)])

        for chunk in loadedChunks:
            chunk.tileGroup.update(self.Player.position)
            chunk.tileGroup.draw(self.screen)

        self.screen.blit(self.Player.playerAnim, (dataTypes.w/2, dataTypes.h/2))

        p.display.update()

    def Load(self, name):
        # TEMP - load player save
        self.saveData = loadSave(name)
        #print(self.saveData.return_save())

        # create Player and world objects from passed data by the loadsave
        self.Player = Player.player(self.saveData.player)
        self.World = world.world(seed=self.saveData.world.seed)


#declaring game client
gameClient = Client()
gameClient.run()