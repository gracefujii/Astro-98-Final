import pygame as pg








def game ():  #main game function
    pg.init()
    global(clock,display)  #global variables to be used in other functions
    clock=pg.time.clock()
    display=pg.display.set_mode(windowwidth,windowheight)  #show the game screen
    mousex=o
    mousey=o
    gameboard=getrandomizedboard()
    revealedboxes=generaterevealedboxesdata(False)
    display.fill()   #add color background
    firstchoice=none
    startgameanimation(gameboard)  #flash symbols underneath boxes
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
                drawhighlightbox (box_x,box_y)   #highlight box
            if not revealedboxes[box_x][box_y] and click:  #if box is covered and clicke
                revealboxesanimation (gameboard,[(box_x,box_y)])  #reveal box
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
                        gamewonanimation(gameboard)
                        pg.time.wait(2000)
                    
                        gameboard=getrandomizedboard()     #restart game, remix board
                        revealedboxes=generaterevealedboxesdata(False)
                        drawboard(gameboard,revealedboxes)  #show board
                        pg.display.update()
                        pg.time.wait(1000)
                        startgameanimation(gameboard)
                    firstchoice=none
                
                
                
                
