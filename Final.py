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
        for event in pg.event.get()
            if event.type==QUIT
                pg.quit()
                sys.exit()
        
