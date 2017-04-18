import pygame as pg






def randomizeboard():
    symbols=[]
    For color in allcolors:
        For shape in allshapes:
            symbols.append((shape,color))  #each item or symbol consist of two attributes (shape, color)
    random.shuffle(symbols) #randomize symbols list
    x=int(boardwitdth*boardlength/2)  #number of symbols used
    symbols=symbols[:x]*2  #double
    random.shuffle(symbols) #randomize symbols list again since doubled
    board=[]
    for x in range(boardwidth):
        column=[]
        for y in range(boardheight):
            column.append(symbol [0])
    
def game ():  #main game function
    pg.init()  #initiate pygame
    global(clock,display)  #global variables to be used in more functions
    clock=pg.time.clock()
    display=pg.display.set_mode(windowwidth,windowheight)  #show the game screen
    mousex=o
    mousey=o
    gameboard=randomizeboard()  #function to randomize board
    revealedboxes=generaterevealedboxesdata(False)  #all boxes unrevealed
    display.fill()   #add color background
    firstchoice=none
    startgameanimation(gameboard)  #function to flash symbols underneath boxes
    while true:
        click=false
        display.fill() #fill screen to cover
        drawboard(gameboard,revealedboxes)
        for event in pg.event.get():
            if event.type==QUIT   #if hit quit, quit
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
                drawhighlightbox (box_x,box_y)   #highlight box function
            if not revealedboxes[box_x][box_y] and click:  #if box is covered and clicke
                revealboxes (gameboard,[(box_x,box_y)])  #reveal box
                revealedboxes[box_x][box_y]=true  #set box as revealed
                if firstchoice==none:  #if first box clicked..
                    firstchoice= (box_x,box_y)  #save first choice details
                else:    #if second box chosen
                    shape1,color1= getshapeandcolor(gameboard, firstchoice[0], firstchoice[1])  #get shapes ans colors of boxes uncovered
                    shape2,color2= getshapeandcolor(gameboard, box_x, box_y)
                    if shape1!= shape2 or color1 != color2   #if the symbols do not match...
                        pg.time.wait(1000)   #pause for moment so player can see symbols don't match
                        coverboxesanimation(gameboard,[(firstchoice[0],firstchoice[1]),(box_x,box_y)])  #cover boxes up
                        revealedboxes[firstchoice[0]][firstchoice[1]]=false   #first choice box now unrevealed till next click
                        revealedboxes[box_x][box_y]=false   #same for second choice
                    elif win(revealedboxes):  #if symbols match then check if all boxes uncovered with win function
                        gamewonanimation(gameboard) #function for animation if won
                        pg.time.wait(2000)
                    
                        gameboard=randomizeboard()     #restart game, remix board
                        revealedboxes=generaterevealedboxesdata(False)
                        drawboard(gameboard,revealedboxes)  #function to show board
                        pg.display.update()
                        pg.time.wait(1000)
                        startgameanimation(gameboard)
                    firstchoice=none
            pg.display.update
            clock.tick(fps)
           

                
                
                
