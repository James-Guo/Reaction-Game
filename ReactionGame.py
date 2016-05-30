import random
import pygame
import sys
import pygame.mixer
from pygame.locals import *

FPS = 30   # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels

# Colours used
RED = (255,   0,   0)
WHITE = (255, 255, 255)

global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Reaction Game')
DISPLAYSURF.fill(WHITE)


points = 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)

beep = pygame.mixer.Sound('Beep.wav')

def playSound():
    beep.play()


def drawCircle():
    x = random.randint(0, WINDOWWIDTH)
    if x < 200:
        y = random.randint(75, WINDOWHEIGHT)
    elif x > WINDOWWIDTH - 200:
        y = random.randint(0, WINDOWHEIGHT - 75)
    else:
        y = random.randint(0, WINDOWHEIGHT)

    pygame.draw.circle(DISPLAYSURF, RED, (x, y), 10, 0)
    print(x, y)


def getColour(x, y):
    return DISPLAYSURF.get_at((x, y))


def checkIfOnCircle(x, y):
    return (DISPLAYSURF.get_at((x, y)) == RED)


def printScore():
    pointsStr = str(points)
    textSurfaceObj = fontObj.render(str('Score: ' + pointsStr), True, RED, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WINDOWWIDTH - 100, WINDOWHEIGHT - 50)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def main():
    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    printScore()
    drawCircle()

    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    timer = 2
    pygame.time.set_timer(USEREVENT + 1, 1000)  # Used to correctly implement seconds

    while True:
        timer_display = font.render("Timer: " + str(timer), 1, (0, 0, 0))
        pygame.draw.rect(DISPLAYSURF, WHITE, (8, 20, 190, 50))
        DISPLAYSURF.blit(timer_display, (10, 30))

        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == USEREVENT + 1:
                timer -= 1


        if mouseClicked is True:
            # If clicked on circle
            if (checkIfOnCircle(x=mousex, y=mousey) is True):
                global points
                points += 1
                DISPLAYSURF.fill(WHITE)
                drawCircle()
                printScore()
                playSound()
                if timer < 3:
                    timer += 1

        if timer <= 0:
            DISPLAYSURF.fill(WHITE)
            gameover_display = fontObj.render('Game over!', True, RED, WHITE)
            DISPLAYSURF.blit(gameover_display, (WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
