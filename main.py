import pygame
pygame.init()
#import startscreen
import Player
import db
import dataTypes
import item
import world
import json
import enemy
import methods
import random

# TODO LIST - make someone say mada mada
#for miller
# TODO LIST - hand_Okay
#for daniel

#init pygame
p = pygame

#create a database interface
dbInt = db.DBInterface()

#another shortcut
pos = dataTypes.pos

#define color constants for easy access
WHITE = dataTypes.WHITE
BLACK = dataTypes.BLACK
RED = dataTypes.RED
GREEN = dataTypes.GREEN
BLUE = dataTypes.BLUE

#easy acces to display and clock
display = p.display
clock = p.time.Clock()

#reference to the save method
save = dbInt.save

#DATA BASE METHODS
#generate new save (compiles all information then writes to db)
def GenerateNewSave(playerName, playerClass):
    player = Player.generateNewPlayerData(playerClass)
    worldData = dataTypes.worldData()

    saveData = dataTypes.saveData(player, worldData).return_save()
    dbInt.newSave(playerName, saveData)

#loads a save then return the parsed save data
def loadSave(saveName):
    save = dbInt.checkSave(saveName)
    return ParseSaveData(json.loads(save.userdata))

#parses the save data and returns it as a saveData object for easy use
def ParseSaveData(saveData):
    player = dataTypes.playerData(
        pos(saveData[0]['pos']['x'], saveData[0]['pos']['y']),
        dataTypes.playerInventory(weapon=item.ItemStack(1, item.allItems[saveData[0]['inv']['weapon']]), special=item.ItemStack(1, item.allItems[saveData[0]['inv']['special']]), armour=item.ItemStack(1, item.allItems[saveData[0]['inv']['armour']]), ring=item.ItemStack(1, item.allItems[saveData[0]['inv']['ring']]), container=dataTypes.container(30, saveData[0]['inv']['container'])),
        dataTypes.entityStats(hp=saveData[0]['stats']['hp'], mp=saveData[0]['stats']['mp'], defen=saveData[0]['stats']['def'] ,spd=saveData[0]['stats']['spd'], atk=saveData[0]['stats']['atk'], dex=saveData[0]['stats']['dex'], vit=saveData[0]['stats']['vit']),
        Player.className[saveData[0]['class']]
    )
    worldData = dataTypes.worldData(saveData[1]['seed'])

    return dataTypes.saveData(player, worldData)

#main client object
class Client:
    #define constants
    running = True

    def __init__(self):
        #initialize pygame and the screen
        self.screen = p.display.set_mode((800, 800))#, pygame.FULLSCREEN)
        pygame.display.set_caption('Dungeon Explorer')  # Title on the title bar of the screen

        self.state = 1

        self.states = {1: self.main_menu, 2:self.game}

        #initialize items
        item.init()

        self.name = None

        #genned Chunks dict to easily store all genned chunks for easy reuse
        self.gennedChunks = {}

    def run(self):
        #main game loop
        while self.running:
            clock.tick(dataTypes.FPS)

            self.states[self.state]()

        #once while loop broken
        p.quit()
        return

    def main_menu(self):
        load = True

        menuState = 1 #1 is main menu, 2 is play menu

        gennedChunks = {}
        loadedChunks = []

        World = world.world(random.randint(1, 10000))

        toGen = dataTypes.pos(-1, -1)
        genTemp = dataTypes.pos(toGen.x, toGen.y)

        for y in range(3):
            genTemp.y = toGen.y + y
            genTemp.x = toGen.x
            for x in range(3):
                genTemp.x = toGen.x + x
                if str(genTemp) not in gennedChunks.keys():
                    gennedChunks[str(genTemp)] = world.Chunk(dataTypes.chunkData(genTemp))
                    gennedChunks[str(genTemp)].genChunk(World.genNoiseMap(gennedChunks[str(genTemp)].tilePos))
                loadedChunks.append(gennedChunks[str(genTemp)])

        buttons1 = p.sprite.Group()
        buttons1.add(methods.playButton(dataTypes.w//2, 400))

        buttons2Load = p.sprite.Group()
        buttons2NewSave = p.sprite.Group()

        buttons3 = p.sprite.Group()
        buttons3.add(methods.createSaveButton(dataTypes.w//2, dataTypes.h//4+dataTypes.h//2))
        buttons3Next = p.sprite.Group()
        buttons3Next.add(methods.nextButton(dataTypes.w//2-130, dataTypes.h//4+227, "L", fonts=[dataTypes.GUI_FONT, dataTypes.GUI_FONT_BUTTON]))
        buttons3Next.add(methods.nextButton(dataTypes.w // 2 + 75, dataTypes.h // 4 + 226, "R", fonts=[dataTypes.GUI_FONT, dataTypes.GUI_FONT_BUTTON]))
        buttons3Back = p.sprite.Group()
        buttons3Back.add(methods.backButton(dataTypes.w//2, dataTypes.h//4+dataTypes.h//2+100))

        saves = 5

        temp = 0

        menuSwapped = False

        accs = []

        for x in dbInt.returnAllSaves():
            buttons2Load.add(methods.loadButton(dataTypes.w // 2, 300 + temp * 100, x.name, fonts=[dataTypes.GUI_FONT, dataTypes.GUI_FONT_BUTTON]))
            accs.append(x.name)
            temp += 1
            saves -= 1

        for y in range(saves):
            buttons2NewSave.add(methods.newSaveButton(dataTypes.w//2, 300+temp*100+y*100, fonts=[dataTypes.GUI_FONT, dataTypes.GUI_FONT_BUTTON]))

        TextField = []
        classes = [Player.warriorClass, Player.mageClass, Player.rangerClass]
        classesIndex = 0

        errorMessages = []

        while load:
            for e in pygame.event.get():
                if e.type == p.QUIT:
                    quit()
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        quit()
                if e.type == p.MOUSEBUTTONDOWN and e.button == 1:  # if it is a click
                    mouse = p.mouse.get_pos()  # get mouse position
                    if not menuSwapped and menuState == 1:
                        for x in buttons1:  # for each button on screen 1
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):  # if it is on a button and it it is o the r
                                menuState = 2
                                menuSwapped = True
                    if menuState == 2 and not menuSwapped:
                        for x in buttons2Load:
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):
                                self.Load(x.text)
                                load = False
                                menuSwapped = True
                        for x in buttons2NewSave:
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):
                                menuState = 3
                                menuSwapped = True
                                TextField = []
                    if menuState == 3 and not menuSwapped:
                        for x in buttons3:
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):
                                if len(TextField) > 0:
                                    if "".join(TextField) not in accs:
                                        GenerateNewSave("".join(TextField), classes[classesIndex])
                                        self.Load("".join(TextField))
                                        load=False
                        for x in buttons3Next:
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):
                                classesIndex = x.press(classesIndex)
                        for x in buttons3Back:
                            if (x.x + x.w > mouse[0] > x.x) and (x.y + x.h > mouse[1] > x.y):
                                TextField = []
                                classesIndex = 0
                                menuState = 2
                if menuState == 3:
                    if e.type == p.KEYDOWN:
                        if e.key == p.K_BACKSPACE:
                            if len(TextField) > 0:
                                TextField.pop()
                        elif e.key == p.K_SPACE:
                            TextField.append(" ")
                        else:
                            TextField.append(pygame.key.name(e.key))


                if e.type == p.MOUSEBUTTONUP:
                    menuSwapped = False

            clock.tick(dataTypes.FPS)

            if menuState == 1:
                for chunk in loadedChunks:
                    chunk.tileGroup.draw(self.screen)

                methods.text_to_screen("DUNGEON EXPLORER", dataTypes.w//2, 200, self.screen, font=dataTypes.GAME_FONT_BIG)
                buttons1.update(self.screen)

            elif menuState == 2:
                for chunk in loadedChunks:
                    chunk.tileGroup.draw(self.screen)
                methods.text_to_screen("DUNGEON EXPLORER", dataTypes.w // 2, 200, self.screen, font=dataTypes.GAME_FONT_BIG)
                buttons2NewSave.update(self.screen)
                buttons2Load.update(self.screen)

            elif menuState == 3:
                for chunk in loadedChunks:
                    chunk.tileGroup.draw(self.screen)
                methods.text_to_screen("Create New Character", dataTypes.w // 2, 200, self.screen, font=dataTypes.GAME_FONT_BIG)
                methods.text_to_screen("- Name -", dataTypes.w//2, dataTypes.h//4+100, self.screen, font=dataTypes.GUI_FONT)
                methods.text_to_screen("".join(TextField), dataTypes.w//2, dataTypes.h//4+150, self.screen, center=True, font=dataTypes.GUI_FONT)
                methods.text_to_screen(classes[classesIndex].name, dataTypes.w//2, dataTypes.h//4 +250, self.screen, center=True, font=dataTypes.GUI_FONT)
                buttons3.update(self.screen)
                buttons3Back.update(self.screen)
                buttons3Next.update(self.screen)

            display.update()

        self.state = 2

    def game(self):
        #allChunks = [_.split(":") for _ in self.gennedChunks.keys()]
        #allChunks = [[int(allChunks[x][0]), int(allChunks[x][1])] for x in range(len(allChunks))]
        for e in p.event.get():  # event queue
            if e.type == p.QUIT:
                self.running = False
                if self.name:
                    dbInt.save(self.name, dataTypes.saveData(self.Player.return_playerData(), self.World.returnWorldData()).return_save())
            if e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    self.running = False
                    if self.name:
                        dbInt.save(self.name, dataTypes.saveData(self.Player.return_playerData(), self.World.returnWorldData()).return_save())
            if e.type == pygame.USEREVENT+1:
                self.Player.Fire(pygame.mouse.get_pos())

        loadedChunks = []

        self.screen.fill(dataTypes.BLACK)

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

        for coords in list(self.gennedChunks):
            temp = [int(_) for _ in coords.split(":")]
            if (((temp[0] - self.Player.chunkPos.x)**2 + (temp[1] - self.Player.chunkPos.y)**2)**0.5) > 4:
                del self.gennedChunks[coords]

        self.Player.bullets.update(self.screen)
        #check for colosion between bullet gorups
        #deal damage to object collided with

        self.screen.blit(self.Player.playerAnim, (dataTypes.w/2-16 + self.Player.drawOffset, dataTypes.h/2-16))

        #gui
        if self.Player.inventory.weapon.material.image:
            self.screen.blit(self.Player.inventory.weapon.material.image, (dataTypes.w//4+100, 750))
        if self.Player.inventory.special.material.image:
            self.screen.blit(self.Player.inventory.special.material.image, (dataTypes.w//4+200, 750))
        if self.Player.inventory.armour.material.image:
            self.screen.blit(self.Player.inventory.armour.material.image, (dataTypes.w//4+300, 750))
        if self.Player.inventory.ring.material.image:
            self.screen.blit(self.Player.inventory.ring.material.image, (dataTypes.w//4+400, 750))

        self.Player.update(self.screen)

        p.display.update()

    def testing(self):
        load = True
        while load:
            for e in pygame.event.get():
                if e.type == p.QUIT:
                    load = False
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        load = False

    def Load(self, name):
        # TEMP - load player save
        self.saveData = loadSave(name)
        self.name = name
        #print(self.saveData.return_save())

        # create Player and world objects from passed data by the loadsave
        self.Player = Player.player(self.saveData.player)
        self.World = world.world(seed=self.saveData.world.seed)


#declaring game client
gameClient = Client()
gameClient.run()
