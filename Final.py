import pygame as pg
import random

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
LINE = 'line'
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
allshapes = (CIRCLE,SQUARE,LINE,ELLIPSE)
bgcolor = WHITE
bgcolor2 = TEAL
boxcolor = BLUE
boxcolor2 = GRAY

def drawIcon(shape,color,boxx,boxy):
    quart = int(boxsize * .25)
    half = int(boxsize * .5)
    left, top = leftTopCoordsOfBox(boxx, boxy) # get coordinates from board 
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
        
def getshapeandcolor(gameboard,boxx,boxy):
    return board[boxx][boxy][0],board[boxx][boxy][1]
        
def splitgroups(groupsize,thelist):
    result = []
    for i in range(0,len(thelist),groupsize):
        result.append(theList[i:i + groupsize])
    return result

def lefttopcoords(boxx,boxy):
    left = boxx * (boxsize + gapsize) + xmargin
    top = boxy * (boxsize + gapsize) + ymargin
    return (left,top)

def getboxatpixel(x,y):
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = lefttopcoords(boxx,boxy)
            boxRect = pg.Rect(left,top,boxsize,boxsize)
            if boxRect.collidepoint(x,y):
                return (boxx, boxy)
    return(None,None)

def boxesdata(x):
    revealedboxes=[]
    for i in range(boardwidth):
        revealedboxes.append([x]*boardheight)
    return revealedboxes

def boxcovers(board,boxes,coverage):
    for box in boxes:
        left,top = lefttopcoords(box[0],box[1])
        pg.draw.rect(display,bgcolor,(left,top,boxsize,boxsize))
        shape,color = getshapeandcolor(board,box[0],box[1])
        drawicon(shape,color,box[0],box[1])
        if coverage > 0:
            pg.draw.rect(display,boxcolor2,(left,top,coverage,boxsize))
    pg.display.update()
    fpsclock.tick(fps)
            
def revealboxes(gameboard,boxestoreveal):
    for coverage in range(boxsize,(-revealspeed) - 1, -revealspeed):
        drawboxcovers(gameboard,boxestoreveal,coverage)

def coverboxes(gameboard,boxestocover):
    for coverage in range(0,boxsize + revealspeed,revealspeed):
        drawboxcovers(gameboard,boxestocover,coverage)

def drawboard(gameboard,revealedboxes):
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = lefttopcoords(boxx,boxy)
            if not revealed[boxx][boxy]:
                pg.draw.rect(display,boxcolor,(left,top,boxsize,boxsize))
            else:
                shape,color = getshapeandcolor(gameboard,boxx,boxy)
                drawicon(shape,color,boxx,boxy)
                
def highlightbox(boxx,boxy):
    left,top = lefttopcoords(boxx,boxy)
    pg.draw.rect(display,bgcolor,(left - 5, top - 5,boxsize + 10,boxsize + 10), 4)
    
    
def randomizeboard():
    symbols=[]
    for color in allcolors:
        for shape in allshapes:
            symbols.append((shape,color))  #each item or symbol consist of two attributes (shape, color)
    random.shuffle(symbols) #randomize symbols list
    x=int(boardwidth*boardheight/2)  #number of symbols used
    symbols=symbols[:x]*2  #double
    random.shuffle(symbols) #randomize symbols list again since doubled
    board=[]
    for x in range(boardwidth):
        column=[]
        for y in range(boardheight):
            column.append(symbols [0])
    
def startgame(gameboard):
    coveredboxes = generaterevealedboxesdata(False)
    boxes = []
    for x in range(boardwidth):
        for y in range(boardheight):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxgroups = splitintogroupsof(6,boxes)
    drawboard(gameboard,coveredboxes)
    for boxgroup in boxgroups:
        revealboxesanimation(gameboard,boxgroup)
        coverboxesanimation(gameboard,boxgroup)
    
def gamewon(gameboard):
    coveredboxes = generaterevealedboxesdata(True)
    color1 = bgcolor
    color2 = bgcolor2
    for i in range(13):
        color1,color2 = color2,color1
        display.fill(color1)
        drawboard(board,coveredboxes)
        pg.display.update()
        pg.time.wait(300)
        
def win(revealedboxes):
    for i in revealedboxes:
        if False in i:
            return False
    return True

def game():  #main game function
    pg.init()  #initiate pygame
    global clock,display  #global variables to be used in more functions
    clock=pg.time.clock() #clock from pygame
    display=pg.display.set_mode(windowwidth,windowheight)  #show the game screen
    mousex=0
    mousey=0
    gameboard=randomizeboard()  #function to randomize board
    revealedboxes=boxesdata(False)  #all boxes unrevealed
    display.fill(bgcolor)   #add color background
    firstchoice=none
    startgame(gameboard)  #function to flash symbols underneath boxes
    while true:
        click=false
        display.fill(bgcolor) #fill screen to cover
        drawboard(gameboard,revealedboxes)
        for event in pg.event.get():
            if event.type==QUIT:   #if hit quit, quit
                pg.quit()
                sys.exit()
            elif event.type== mousemotion: #otherwise if mouse moves..
                mousex, mousey= event.pos  #update mouse postion
            elif event.type== mousebuttonup: # or if mouse was clicked
                mousex, mousey== mousemotion
                click=true
        box_x,box_y=getboxatpixel(mousex, mousey)
        if box_x==none and box_y==none:   #if mouse over box
            if not revealedboxes[box_x][box_y]:  #if box is covered
                highlightbox (box_x,box_y)   #highlight box function
            if not revealedboxes[box_x][box_y] and click:  #if box is covered and clicke
                revealboxes (gameboard,[(box_x,box_y)])  #reveal boxes function
                revealedboxes[box_x][box_y]=true  #set box as revealed
                if firstchoice==none:  #if first box clicked..
                    firstchoice= (box_x,box_y)  #save first choice details
                else:    #if second box chosen
                    shape1,color1= getshapeandcolor(gameboard, firstchoice[0], firstchoice[1])  #get shapes ans colors of boxes uncovered
                    shape2,color2= getshapeandcolor(gameboard, box_x, box_y)
                    if shape1!= shape2 or color1 != color2:   #if the symbols do not match...
                        pg.time.wait(1000)   #pause for moment so player can see symbols don't match
                        coverboxes(gameboard,[(firstchoice[0],firstchoice[1]),(box_x,box_y)])  #cover boxes up
                        revealedboxes[firstchoice[0]][firstchoice[1]]=false   #first choice box now unrevealed till next click
                        revealedboxes[box_x][box_y]=false   #same for second choice
                    elif win(revealedboxes):  #if symbols match then check if all boxes uncovered with win function
                        gamewonanimation(gameboard) #function for animation if won
                        pg.time.wait(2000)
                    
                        gameboard=randomizeboard()     #restart game, remix board
                        revealedboxes=boxesdata(False)
                        drawboard(gameboard,revealedboxes)  #function to show board
                        pg.display.update()
                        pg.time.wait(1000)
                        startgame(gameboard)
                    firstchoice=none
            pg.display.update
            clock.tick(fps)
           

                
                
                
