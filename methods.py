import pygame
import dataTypes

WHITE = dataTypes.WHITE
GAME_FONT = dataTypes.GAME_FONT
GAME_FONT2 = dataTypes.GAME_FONT2

#button object
#for reuse of easy buttoning
class button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def press(self, *args, **kwargs):
        pass

    def update(self, screen):
        mouse = pygame.mouse.get_pos()

        if ((self.x + self.w) > mouse[0] > self.x) and ((self.y + self.h) > mouse[1] > self.y):
            text_to_screen(self.text, self.x+self.w//2, self.y+self.h//2, screen, center=True)
        else:
            text_to_screen(self.text, self.x+self.w//2, self.y+self.h//2, screen, center=True, font=GAME_FONT2)

class playButton(button):
    def __init__(self, x, y):
        super().__init__(x-75, y, 150, 50, "Play")

class loadButton(button):
    def __init__(self, x, y, loadName):
        super().__init__(x-75, y, 150, 50, loadName)

    def press(self, method, name):
        method(name)

class newSaveButton(button):
    def __init__(self, x, y):
        super().__init__(x-100, y, 200, 50, "New Save")

    #def press(self, ): swap to save creation screen

def text_obj(text, font):
    textSurface = font.render(text, True, dataTypes.WHITE)
    return textSurface, textSurface.get_rect()

def text_to_screen(text, x, y, surface, font=dataTypes.GAME_FONT, center=True):
    textSurf, textRect = text_obj(text, font)
    if center:
        textRect.center = (x, y)
    if not center:
        textRect.x, textRect.y = (x, y)
    surface.blit(textSurf, textRect)