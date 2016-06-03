import random
import pygame
import sys
import pygame.mixer
from pygame.locals import *

FPS = 30   # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels

# Colours used
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARK_RED = (200, 0, 0)

HIGHLIGHTCOLOUR = DARK_RED
CIRCLECOLOUR = RED


global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Reaction Game')
DISPLAYSURF.fill(WHITE)

points = 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)

beep = pygame.mixer.Sound('Beep.wav')

PAUSE = False


def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def playSound():
    beep.play()


def drawCircle(x, y, clicked):
    if clicked is True:
        pygame.draw.circle(DISPLAYSURF, WHITE, (x, y), 10, 0)
        x = random.randint(0, WINDOWWIDTH)
        if x < 200:
            y = random.randint(75, WINDOWHEIGHT)
        elif x > WINDOWWIDTH - 200:
            y = random.randint(0, WINDOWHEIGHT - 75)
        else:
            y = random.randint(0, WINDOWHEIGHT)

    pygame.draw.circle(DISPLAYSURF, CIRCLECOLOUR, (x, y), 10, 0)

    return x, y


def drawTimer(timer):
    font = pygame.font.SysFont('Consolas', 30)
    timer_display = font.render("Timer: " + str(timer), 1, (0, 0, 0))
    pygame.draw.rect(DISPLAYSURF, WHITE, (8, 20, 190, 50))
    DISPLAYSURF.blit(timer_display, (10, 30))


def getColour(x, y):
    return DISPLAYSURF.get_at((x, y))


def checkIfOnCircle():
    mouse = pygame.mouse.get_pos()
    return (DISPLAYSURF.get_at((mouse[0], mouse[1])) == CIRCLECOLOUR)


def printScore():
    pointsStr = str(points)
    textSurfaceObj = fontObj.render(str('Score: ' + pointsStr), True, CIRCLECOLOUR, WHITE)
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


def unpause():
    global PAUSE
    PAUSE = False

def pause():
    while PAUSE:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        DISPLAYSURF.fill(WHITE)
        gameover_display = fontObj.render('Game paused!', True, RED, WHITE)
        DISPLAYSURF.blit(gameover_display, (220, 150))
        button("Continue", 230, 300, 190, 50, WHITE, RED, "unpause")
        button("Main Menu", 230, 350, 190, 50, WHITE, RED, "menu")
        button("Quit", 230, 400, 190, 50, WHITE, RED, "quit")

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    DISPLAYSURF.fill(WHITE)
    printScore()




def arcadeMode():
    circleX = 0
    circleY = 0
    printScore()
    circleX, circleY = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    global PAUSE

    timer = 30
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(timer)

        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    pause()
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            elif event.type == USEREVENT + 1:
                timer -= 1

        if mouseClicked is True:
            # If clicked on circle
            if (checkIfOnCircle() is True):
                global points
                points += 1
                circleX, circleY = drawCircle(circleX, circleY, True)
                printScore()
                playSound()

        if timer <= 0:
            drawGameOver()

        circleX, circleY = drawCircle(circleX, circleY, False)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def survivalMode():
    circleX = 0
    circleY = 0

    printScore()
    circleX, circleY = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    global PAUSE
    timer = 2
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(timer)
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    pause()
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            elif event.type == USEREVENT + 1:
                timer -= 1

        if mouseClicked is True:
            # If clicked on circle
            if (checkIfOnCircle() is True):
                global points
                points += 1
                circleX, circleY = drawCircle(circleX, circleY, True)
                printScore()
                playSound()
                if timer < 2:
                    timer += 1

        if timer <= 0:
            drawGameOver()

        circleX, circleY = drawCircle(circleX, circleY, False)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawOptions():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        colourSelectionButton(230, 150, 50, 50, RED)
        colourSelectionButton(300, 150, 50, 50, ORANGE)
        colourSelectionButton(370, 150, 50, 50, YELLOW)
        colourSelectionButton(230, 220, 50, 50, GREEN)
        colourSelectionButton(300, 220, 50, 50, BLUE)
        colourSelectionButton(370, 220, 50, 50, PURPLE)

        button("Main Menu", 230, 350, 190, 50, WHITE, RED, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawMenu():
    global points, PAUSE
    PAUSE = False
    points = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        button("Arcade", 230, 150, 190, 50, WHITE, RED, "arcade")
        button("Survival", 230, 200, 190, 50, WHITE, RED, "survival")
        button("Options", 230, 250, 190, 50, WHITE, RED, "options")
        button("Quit", 230, 300, 190, 50, WHITE, RED, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def colourSelectionButton(x, y, w, h, colour):
    global CIRCLECOLOUR

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    drawButtonBorder(x, y, w, h)

    if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
        #  If on the button and clicked
        CIRCLECOLOUR = colour

    pygame.draw.rect(DISPLAYSURF, colour, (x, y, w, h))


def button(msg, x, y, w, h, inactiveColour, activeColour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
         # if mouse is inside the box
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
            elif action == "options":
                DISPLAYSURF.fill(WHITE)
                drawOptions()
            elif action == "unpause":
                unpause()
            elif action == "quit":
                pygame.quit()
                sys.exit()

    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColour, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)



def drawButtonBorder(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    # if mouse is inside the box
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x - 5, y - 5, w + 10, h + 10), 4)


def main():
    drawMenu()


if __name__ == '__main__':
    main()
