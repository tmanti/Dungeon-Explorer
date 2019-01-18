import pygame
import dataTypes

WHITE = dataTypes.WHITE
GAME_FONT = dataTypes.GAME_FONT
GAME_FONT2 = dataTypes.GAME_FONT2

#button object
#for reuse of easy buttoning
class button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, box=True):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text

        self.normal = pygame.Surface((200,200))
        text_to_screen(text, 5, 5, self.normal, center=False)

        self.hover = pygame.Surface((200,200))
        text_to_screen(text, 5, 5, self.hover, center=False, font=GAME_FONT2)

        self.pressed = pygame.Surface((200,200))
        text_to_screen(text, 5, 5, self.pressed, center=False, font=GAME_FONT2)

    def press(self):
        pass

    def update(self, screen, hover=False, pressed=False):
        if hover:
            screen.blit(self.hover, (self.x, self.y))
        elif pressed:
            screen.blit(self.pressed, (self.x, self.y))
        else:
            screen.blit(self.normal, (self.x-self.normal.get_size()[0]//2, self.y))

class playButton(button):
    def __init__(self, x, y):
        super().__init__(x, y, "Play", box=False)

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