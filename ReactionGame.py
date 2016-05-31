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
BLACK = (0, 0, 0)

DARK_RED = (200, 0, 0)

global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Reaction Game')
DISPLAYSURF.fill(WHITE)


points = 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)

beep = pygame.mixer.Sound('Beep.wav')


def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


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


def checkIfOnCircle():
    mouse = pygame.mouse.get_pos()
    return (DISPLAYSURF.get_at((mouse[0], mouse[1])) == RED)


def printScore():
    pointsStr = str(points)
    textSurfaceObj = fontObj.render(str('Score: ' + pointsStr), True, RED, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WINDOWWIDTH - 100, WINDOWHEIGHT - 50)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawGameOver():
    DISPLAYSURF.fill(WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        gameover_display = fontObj.render('Game over!', True, RED, WHITE)
        DISPLAYSURF.blit(gameover_display, (WINDOWWIDTH/2 - 80, WINDOWHEIGHT/2 - 25))
        printScore()
        button("Main Menu", 230, 350, 190, 50, WHITE, RED, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def arcadeMode():
    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    printScore()
    drawCircle()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    timer = 30
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

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
            if (checkIfOnCircle() is True):
                global points
                points += 1
                DISPLAYSURF.fill(WHITE)
                drawCircle()
                printScore()
                playSound()

        if timer <= 0:
            drawGameOver()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def survivalMode():
    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    printScore()
    drawCircle()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    timer = 2
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

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
            if (checkIfOnCircle() is True):
                global points
                points += 1
                DISPLAYSURF.fill(WHITE)
                drawCircle()
                printScore()
                playSound()
                if timer < 2:
                    timer += 1

        if timer <= 0:
            drawGameOver()

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def drawMenu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        button("Arcade", 230, 200, 190, 50, WHITE, RED, "arcade")
        button("Survival", 230, 250, 190, 50, WHITE, RED, "survival")
        button("Quit", 230, 300, 190, 50, WHITE, RED, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def button(msg, x, y, w, h, inactiveColour, activeColour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)
    # if mouse is inside the box
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, activeColour, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if action == "survival":
                DISPLAYSURF.fill(WHITE)
                survivalMode()
            elif action == "arcade":
                DISPLAYSURF.fill(WHITE)
                arcadeMode()
            elif action == "menu":
                DISPLAYSURF.fill(WHITE)
                drawMenu()
            elif action == "quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColour, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ((x + (w/2), (y + (h/2))))
    DISPLAYSURF.blit(textSurf, textRect)


def main():
    drawMenu()


if __name__ == '__main__':
    main()
