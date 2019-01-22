import pygame
import dataTypes

WHITE = dataTypes.WHITE

#button object
#for reuse of easy buttoning
class button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, font=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.fonts = font

    def press(self, *args, **kwargs):
        pass

    def update(self, screen):
        mouse = pygame.mouse.get_pos()

        if ((self.x + self.w) > mouse[0] > self.x) and ((self.y + self.h) > mouse[1] > self.y):
            text_to_screen(self.text, self.x+self.w//2, self.y+self.h//2, screen, center=True, font=self.fonts[0])
        else:
            text_to_screen(self.text, self.x+self.w//2, self.y+self.h//2, screen, center=True, font=self.fonts[1])

class playButton(button):
    def __init__(self, x, y, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-75, y, 150, 50, "Play", font=fonts)

class instructionsButton(button):
    def __init__(self, x, y, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-75, y, 150, 50, "Instructions", font=fonts)

class loadButton(button):
    def __init__(self, x, y, loadName, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-75, y, 150, 50, loadName, font=fonts)

    def press(self, method, name, *args, **kwargs):
        method(name)

class newSaveButton(button):
    def __init__(self, x, y, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-100, y, 200, 50, "- New Save -", font=fonts)

class createSaveButton(button):
    def __init__(self, x, y, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-100, y, 200, 50, "Create", font=fonts)

class nextButton(button):
    def __init__(self, x, y, LR, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x, y, 50, 50, None, font=fonts)
        self.LR = LR
        if LR == "L":
            self.text = "<"
        elif LR == "R":
            self.text = ">"

    def press(self, iterVar, *args, **kwargs):
        if self.LR == "R":
            return (iterVar+1)%3
        if self.LR == "L":
            return (iterVar-1)%3

class backButton(button):
    def __init__(self, x, y, fonts=(dataTypes.GAME_FONT, dataTypes.GAME_FONT_BUTTON)):
        super().__init__(x-50, y, 100, 50, "Back", font=fonts)


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