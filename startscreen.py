#Ali

import pygame
import time

pygame.init()

white = (255, 255, 255) #assigns rgb color values to variables
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800 #sets the screen width
display_height = 600 #sets the screen height

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dungeon Explorer') #Title on the title bar of the screen

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25) #sets the font

def text_objects(text,color,size): #function for diffeent font sizes used
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size = "small"): #function for the text on the screen
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def game_intro(): #while game intro is on this is what's going happen
    intro = True

    while intro:
        # checks for events
        for event in pygame.event.get(): #if someclicks X on top right corner of screen then exit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #if someone presses "c" start game
                    intro = False
                if event.key == pygame.K_q: # if q is pressed then exit out of game
                    pygame.quit()
                    quit()

        gameDisplay.fill(white) # background color is white
        message_to_screen("Dungeon Explorer", green, -100, "medium") #messages to user on the start screen
        message_to_screen("Game's Objective", black, -30)
        message_to_screen("Description", black, 10)
        message_to_screen("Description", black, 50)
        message_to_screen("Press C to Play or Q to Quit", black, 180) # instructions to start or end the game

        pygame.display.update() # updates the screen
        clock.tick(15) # fps of 15
game_intro()
