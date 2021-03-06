import pygame as pg
import random
import sys
from pygame.locals import*

fps = 30
#board parameters
windowwidth = 1000
windowheight = 600
boxsize = 60
gapsize = 10
boardwidth = 8
boardheight = 5
revealspeed = 8
xmargin = int((windowwidth - (boardwidth * (boxsize + gapsize))) / 2)
ymargin = int((windowheight - (boardheight * (boxsize + gapsize))) / 2)

#shapes for the game 
CIRCLE = 'circle'
SQUARE = 'square'
LINES = 'lines'
ELLIPSE = 'ellipse'

#colors    R    G    B
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
GRAY =   ( 80, 100, 120)
BLUE =   (  0, 100, 150)
GREEN =  ( 20, 150, 100)
RED =    (200,  50,  60)
TEAL =   ( 60, 180, 160)
PURPLE = (100,  80, 120)
PEACH =  (240, 180, 160)
YELLOW = (250, 200,  50)

allcolors = (GREEN,RED,PURPLE,PEACH,YELLOW)
allshapes = (CIRCLE,SQUARE,LINES,ELLIPSE)
bgcolor = WHITE
bgcolor2 = TEAL
boxcolor = BLUE
boxcolor2 = GRAY


def game():  #main game function
    pg.init()  #initiate pygame
    global clock,display  #global variables to be used in more functions
    clock = pg.time.Clock() #clock from pygame
    display = pg.display.set_mode((windowwidth,windowheight))  #show the game screen
    mousex = 0 #stores x coord of mouse
    mousey = 0 #stores y coord of mouse
    gameboard = randomizeboard()  #function to randomize board
    revealedboxes = boxesdata(False)  #all boxes unrevealed
    display.fill(bgcolor)   #add color background
    firstchoice = None
    startgame(gameboard)  #function to flash symbols underneath boxes
    while True:
        click = False
        display.fill(bgcolor) #fill screen to cover
        drawboard(gameboard,revealedboxes)
        for event in pg.event.get():
            if event.type == QUIT:   #if hit quit, quit
                pg.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: #otherwise if mouse moves..
                mousex, mousey= event.pos  #update mouse postion
            elif event.type == MOUSEBUTTONUP: # or if mouse was clicked
                mousex, mousey == event.pos
                click = True
        boxx,boxy=getboxatpixel(mousex, mousey)
        if boxx != None and boxy != None:   #if mouse over box
            if not revealedboxes[boxx][boxy]:  #if box is covered
                highlightbox(boxx,boxy)   #highlight box function
            if not revealedboxes[boxx][boxy] and click:  #if box is covered and clicke
                revealboxes(gameboard,[(boxx,boxy)])  #reveal boxes function
                revealedboxes[boxx][boxy] = True  #set box as revealed
                if firstchoice == None:  #if first box clicked..
                    firstchoice = (boxx,boxy)  #save first choice details
                else:    #if second box chosen
                    shape1,color1= getshapeandcolor(gameboard, firstchoice[0], firstchoice[1])  #get shapes ans colors of boxes uncovered
                    shape2,color2= getshapeandcolor(gameboard, boxx, boxy)
                    if shape1!= shape2 or color1 != color2:   #if the symbols do not match...
                        pg.time.wait(1000)   #pause for moment so player can see symbols don't match
                        coverboxes(gameboard,[(firstchoice[0],firstchoice[1]),(boxx,boxy)])  #cover boxes up
                        revealedboxes[firstchoice[0]][firstchoice[1]] = False   #first choice box now unrevealed till next click
                        revealedboxes[boxx][boxy] = False   #same for second choice
                    elif win(revealedboxes):  #if symbols match then check if all boxes uncovered with win function
                        gamewon(gameboard) #function for animation if won
                        pg.time.wait(2000)
                    
                        gameboard=randomizeboard()     #restart game, remix board
                        revealedboxes=boxesdata(False)
                        
                        drawboard(gameboard,revealedboxes)  #function to show board
                        pg.display.update()
                        pg.time.wait(1000)
                        startgame(gameboard)
                    firstchoice = None
                    
        pg.display.update
        clock.tick(fps)

def drawicon(shape,color,boxx,boxy):
    quarter = int(boxsize * .25)
    half = int(boxsize * .5)
    left, top = lefttopcoords(boxx,boxy) # get coordinates from board 
    # to draw the shapes of the things to find. Uses draw method which is pre made.
    if shape == CIRCLE:
        pg.draw.circle(display, color, (left + half, top + half), half - 5)
    elif shape == SQUARE:
        pg.draw.rect(display, color, (left + quarter, top + quarter, boxsize - half, boxsize - half))   
    elif shape == LINES:
        for i in range(0, boxsize, 4):
            pg.draw.line(display, color, (left, top + i), (left + i, top))
            pg.draw.line(display, color, (left + i, top + boxsize - 1), (left + boxsize - 1, top + i))
    elif shape == ELLIPSE:
        pg.draw.ellipse(display, color, (left, top + quarter, boxsize, half))
        
def getshapeandcolor(board,boxx,boxy):
    return board[boxx][boxy][0],board[boxx][boxy][1]
        
def splitgroups(groupsize,thelist):
    #splits list into list of lists
    result = []
    for i in range(0,len(thelist),groupsize):
        result.append(thelist[i:i + groupsize])
    return result

def lefttopcoords(boxx,boxy):
    #convert board coords into pixel coords
    left = boxx * (boxsize + gapsize) + xmargin
    top = boxy * (boxsize + gapsize) + ymargin
    return (left,top)

def getboxatpixel(x,y):
    #
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = lefttopcoords(boxx,boxy)
            boxRect = pg.Rect(left,top,boxsize,boxsize)
            if boxRect.collidepoint(x,y):
                return (boxx, boxy)
    return(None,None)

def boxesdata(x):
    revealedboxes = []
    for i in range(boardwidth):
        revealedboxes.append([x]*boardheight)
    return revealedboxes

def boxcovers(board,boxes,coverage):
    #draws boxes being covered/revealed
    #"boxes" = list of 2-item lists
    for box in boxes:
        left,top = lefttopcoords(box[0],box[1])
        pg.draw.rect(display,bgcolor,(left,top,boxsize,boxsize))
        shape,color = getshapeandcolor(board,box[0],box[1])
        drawicon(shape,color,box[0],box[1])
        if coverage > 0:
            pg.draw.rect(display,boxcolor2,(left,top,coverage,boxsize))
    pg.display.update()
    clock.tick(fps)
            
def revealboxes(board,boxestoreveal):
    #box reveal animation
    for coverage in range(boxsize,(-revealspeed) - 1, -revealspeed):
        boxcovers(board,boxestoreveal,coverage)

def coverboxes(board,boxestocover):
    #box cover animation
    for coverage in range(0,boxsize + revealspeed,revealspeed):
        boxcovers(board,boxestocover,coverage)

def drawboard(board,revealed):
    #draws all boxes in covered/revealed state
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = lefttopcoords(boxx,boxy)
            if not revealed[boxx][boxy]:
                #draw covered box
                pg.draw.rect(display,boxcolor,(left,top,boxsize,boxsize))
            else:
                #draw revealed icon
                shape,color = getshapeandcolor(board,boxx,boxy)
                drawicon(shape,color,boxx,boxy)
                
def highlightbox(boxx,boxy):
    left,top = lefttopcoords(boxx,boxy)
    pg.draw.rect(display,boxcolor2,(left - 5, top - 5,boxsize + 10,boxsize + 10), 4)
    
    
def randomizeboard():
    #get list of every possible shape/color combo
    symbols = []
    for color in allcolors:
        for shape in allshapes:
            symbols.append((shape,color))  #each item or symbol consist of two attributes (shape, color)
    random.shuffle(symbols) #randomize symbols list
    x = int(boardwidth*boardheight/2)  #number of symbols used
    symbols = symbols[:x]*2  #two of each
    random.shuffle(symbols) #randomize symbols list again since doubled
    #create board structure
    board = []
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append(symbols[0])
            del symbols[0] #remove symbols as they are assigned
        board.append(column)
    return board
    
def startgame(board):
    #randomly reveal boxes 5 at a time
    coveredboxes = boxesdata(False)
    boxes = []
    for x in range(boardwidth):
        for y in range(boardheight):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxgroups = splitgroups(5,boxes)
    drawboard(board,coveredboxes)
    for boxgroup in boxgroups:
        revealboxes(board,boxgroup)
        coverboxes(board,boxgroup)
    
def gamewon(board):
    #flash bgcolor when player has won
    coveredboxes = boxesdata(True)
    color1 = bgcolor2
    color2 = bgcolor
    for i in range(13):
        color1,color2 = color2,color1 #swap colors
        display.fill(color1)
        drawboard(board,coveredboxes)
        pg.display.update()
        pg.time.wait(300)
        
def win(revealedboxes):
    #returns true if all boxes revealed
    for i in revealedboxes:
        if False in i:
            return False #return False if any boxes covered
    return True
                
if __name__ == '__main__':
    game()
                
                
