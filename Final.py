import pygame








def game ():  #main game function
    pygame.init()
    global(clock,display)  #global variables to be used in other functions
    clock=pygame.time.clock()
    display=pygame.display.set_mode(windowwidth,windowheight)  #show the game screen
    
    mousex=o
    mousey=o
    gameboard=getrandomizedboard()
    revealedboxes=generaterevealedboxesdata(False)
    
    firstchoice=none
    startgameanimation(gameboard)
    display.fill
