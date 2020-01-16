import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()

def CreateBoard(height, width): # creating board
    board = []
    for x in range(height):
        board.append(["0"] * width)
    n = 1
    for row in board:
        for box in range(width):
            row[box] = n
            n+=1
    return board

# Example of Board --- Here is board of height 2 and width 4 ---- [[1, 2, 3, 4], [5, 6, 7, 8]]

def RowColOf(box,board): # getting row and column number of a box in board
    boxRow = 0
    boxCol = 0
    for scanRow in board: # iterate through board ---- gives row
        boxRow +=1 # row will increase as we iterate through board
        boxCol = 0 # after completing each row we come back to first column of next row
        for scanBox in scanRow: # iterate through row ---- gives box
            boxCol+=1 # column will increase as we iterate through row
            if scanBox == box:
                return (boxRow, boxCol)

def LeftTopOf(box, board): # getting left top coordinates of a box in board
    boxRow , boxCol = RowColOf(box,board)    
    left = boxCol * (BOXSIZE + GAPSIZE) 
    top = boxRow * (BOXSIZE + GAPSIZE)
    return (left,top)            
    
def DrawBoard(board): # drawing board
    for row in board:
        for box in row:
            left,top = LeftTopOf(box, board)
            pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOXSIZE, BOXSIZE))
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~
SCR_HEIGHT = 680
SCR_WIDTH = 600
BOARD_HEIGHT = 5 # number of rows in board
BOARD_WIDTH = 5 # number of columns in board            
BOXSIZE = 80 # length and breadth of box
GAPSIZE = 5 # gap b/w boxes
#-------------- DISPLAY -----------------------------------------
DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Battleship')
#----------------------------------------------------------------
#----COLORS------
BOX_COLOR = (255,0,0)
BGCOLOR = (255, 255, 255)
BGCOLOR = (255, 255, 255) 
GREEN = (0,255,0)
BLUE = (0,0,255)
HOVER_COLOR = (41,41,41)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#----------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# *Initially putting StartButton outside window.
StartButton = pygame.draw.rect(DISPLAYSURF, BLUE, (-200,-200, 200, 80))
def IntroAnimation(x = False): # Animation played when game is started.
    global StartButton # It means if we define any variable named 'StartButton' and change...
    #....its value it will affect our global part of it ie. its initial* value
    if not x:
        return StartButton
    else: # Do not start animation unless x is given -- True
        INTRO_FONT_SIZE = 20 # Font size for 'Battleship' text        
        FontObj = pygame.font.Font('gomarice_kaiju_monster.ttf', INTRO_FONT_SIZE)        
        LetsPlayBattleship = FontObj.render("Battleship!", True, GREEN, WHITE)
        LetsPlayBattleship_Rect = LetsPlayBattleship.get_rect()
        
        for pos in range(SCR_HEIGHT/2): # Animation to change position of text...
            #....from top to middle of screen(SCR_HEIGHT/2).
            # loop changes from zero y coordinate to middle(SCR_HEIGHT/2) y coordinate.
            LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, pos)
            # next we hide the dirt left by the text on coming from top to middle of screen...
            #....by drawing a rectangle with arbitary coordinates which hides the dirt.
            pygame.draw.rect(DISPLAYSURF, WHITE, (250,0, 100, SCR_HEIGHT/2))
            DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
            pygame.display.update() # update screen after each loop
        # After the position of text is in center the text resizes.
        for size in range(20, 120): # loop changes 'INTRO_FONT_SIZE' from 20 to 120
            INTRO_FONT_SIZE = size
            FontObj = pygame.font.Font('gomarice_kaiju_monster.ttf', INTRO_FONT_SIZE)
            LetsPlayBattleship = FontObj.render("Battleship!", True, GREEN, WHITE)
            LetsPlayBattleship_Rect = LetsPlayBattleship.get_rect()
            LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)            
            DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
            pygame.display.update()
        pygame.time.wait(400) # Wait for some time...
        for pos in range(SCR_HEIGHT/2,SCR_HEIGHT/2-100,-1): # 3rd animation, to bring the...
            #....text some coordinates up making space for 'start button'.
            LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, pos)
            pygame.draw.rect(DISPLAYSURF, WHITE, (270,0, 100, SCR_HEIGHT/2))
            DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
            pygame.display.update() # update screen after each loop
        # At last drawing Start Button
        left, top = LetsPlayBattleship_Rect.bottomleft # getting left and top coordinates.....
        #....of intro text
        # placing start button.
        StartButton = pygame.draw.rect(DISPLAYSURF, BLUE, ((SCR_WIDTH/2)-100,top, 200, 80))
        START_FONT_SIZE = 50 # Font size for 'StartButton' text
        FontObj_Start = pygame.font.Font('PoplarStd.otf', START_FONT_SIZE)
        StartButtonText = FontObj_Start.render('START', True, WHITE, BLUE)
        StartButtonText_Rect = StartButtonText.get_rect()
        StartButtonText_Rect.center = StartButton.center
        DISPLAYSURF.blit(StartButtonText, StartButtonText_Rect)
        pygame.display.update()


               
#START_BUTTON_ON = False # Initially StartButton is 'OFF'
DISPLAYSURF.fill(BGCOLOR) # Coloring the window background
'''
#----------------Starting intro animation---------
IntroAnimation(True) # Invoking IntroAnimation (with True ie. Start Animation)
pygame.display.update()
#-------------------------------------------------
'''
    


'''
GREEN = (0,255,0)
BLUE = (0,0,255)
INTRO_FONT_SIZE = 50
            
FontObj = pygame.font.Font('freesansbold.ttf', INTRO_FONT_SIZE) 
LetsPlayBattleship = FontObj.render("Let's play Battleship!", True, GREEN, BLUE) 
LetsPlayBattleship_Rect = LetsPlayBattleship.get_rect()
LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
pygame.display.update()
pygame.time.wait(2000)

DISPLAYSURF.fill((255,255,255))
DrawBoard(board)

pygame.display.update()
'''

def RandomRow(board):
    return randint(1, len(board))

def RandomCol(board):
    return randint(1, len(board[0]))

def MouseCollideSomeBox(mousex, mousey, board): # check if mouse collided...
    #...with any box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(box, board)
            AnyBox = (pygame.Rect(left, top, BOXSIZE, BOXSIZE))
            if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                return True 

def MouseCollideOurBox(mousex, mousey, board, OurRow, OurCol): # check if mouse collided...
    #...with our box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(box, board)
            AnyBox = (pygame.Rect(left, top, BOXSIZE, BOXSIZE))
            if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                if RowColOf(box, board) == (OurRow, OurCol): # now check if box was our box
                    return True                



def DrawHoverBox(mousex, mousey, board):#Draw hover box over a box viz. under mouse coordinates
    for row in board:
        for box in row:
            left,top = LeftTopOf(box, board)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox.collidepoint(mousex, mousey): # if we come up with our box..
                #...draw hover box over it.
                pygame.draw.rect(DISPLAYSURF, HOVER_COLOR, (left, top, BOXSIZE, BOXSIZE))                
                return None # just to stop the box loop and row loop.

def GameOverAnimation():
    # Transparent Overlay
    Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
    Overlay.set_alpha(238)                # alpha level
    Overlay.fill(BLACK)           # this fills the entire surface
    DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates

    GAME_OVER_SIZE = 90 # Font size for 'GameOver' text
    FontObj_Won = pygame.font.Font('PoplarStd.otf', GAME_OVER_SIZE)
    GameOverText = FontObj_Won.render('GAME OVER', True, RED)
    GameOverText_Rect = GameOverText.get_rect()
    GameOverText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
    YOU_LOSE_SIZE = 50
    FontObj_Won = pygame.font.Font('PoplarStd.otf', YOU_LOSE_SIZE)
    YouLoseText = FontObj_Won.render('YOU LOSE', True, RED)
    YouLoseText_Rect = YouLoseText.get_rect()
    YouLoseText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2+90)
    DISPLAYSURF.blit(YouLoseText, YouLoseText_Rect)
    DISPLAYSURF.blit(GameOverText, GameOverText_Rect)
    pygame.display.update()    
    
def GameWonAnimation():
    # Transparent Overlay---------------------------------------------------------
    Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
    Overlay.set_alpha(238)                # alpha level
    Overlay.fill(WHITE)           # this fills the entire surface
    DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
    #-----------------------------------------------------------------------------
    GAME_WON_SIZE = 90 # Font size for 'GameOver' text
    FontObj_Over = pygame.font.Font('PoplarStd.otf', GAME_WON_SIZE)
    GameWonText = FontObj_Over.render('YOU WON', True, BLUE)
    GameWonText_Rect = GameWonText.get_rect()
    GameWonText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
    DISPLAYSURF.blit(GameWonText, GameWonText_Rect)
    pygame.display.update()
def PrintChance(x):
    # Transparent Overlay---------------------------------------------------------
    Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
    Overlay.set_alpha(238)                # alpha level
    Overlay.fill(GREEN)           # this fills the entire surface
    DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
    #-----------------------------------------------------------------------------
    
    #DISPLAYSURF.fill(BGCOLOR)
    CHANCE_SIZE = 50 # Font size for 'GameOver' text
    FontObj_Chance = pygame.font.Font('SHOWG.ttf', CHANCE_SIZE)
    ChanceText = FontObj_Chance.render('CHANCE :'+str(x), True, BLUE)
    ChanceText_Rect = ChanceText.get_rect()
    ChanceText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2+20)
    DISPLAYSURF.blit(ChanceText, ChanceText_Rect)
    pygame.display.update()
    pygame.time.wait(500)
    DISPLAYSURF.fill(BGCOLOR)
    pygame.display.update()
board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
#OurRow = RandomRow(board)
#OurCol = RandomCol(board)



#chance = 0
while True:
    OurRow = RandomRow(board)
    OurCol = RandomCol(board)
    START_BUTTON_ON = False # Initially StartButton is 'OFF'
    chance = 1
    if not START_BUTTON_ON: # Animate intro animation if START_BUTTON is not 'ON'
        DISPLAYSURF.fill(BGCOLOR) # Coloring the window background 
        #----------------Starting intro animation---------
        IntroAnimation(True) # Invoking IntroAnimation (with True ie. Start Animation)
        pygame.display.update()
        #-------------------------------------------------
    DISPLAYSURF.fill(BGCOLOR)
    while not START_BUTTON_ON: # Loop until Start Button is clicked.
        StartButtonText_Rect = IntroAnimation() # Invoking IntroAnimation(with False....)
        #(....ie. return only Start Button rect.)
        for event in pygame.event.get(): # Checking each event happening on window.
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP: # If button was clicked..
                mousex, mousey = event.pos
                if StartButtonText_Rect.collidepoint(mousex, mousey): #..check if StartButton..
                    #...was clicked
                    START_BUTTON_ON = True # Now Start Button is 'ON'
    while START_BUTTON_ON: # Finally Start Button is clicked (or, it is 'ON').
        mouseClicked = False 
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            elif (event.type == KEYDOWN and event.key == K_a):
                left = OurCol * (BOXSIZE + GAPSIZE)+30 
                top = OurRow * (BOXSIZE + GAPSIZE)+30
                Temp = HOVER_COLOR # Storing HOVER_COLOR in temporary variable
                HOVER_COLOR = (210,0,0) # changing HOVER_COLOR(a bit light).
                DrawHoverBox(left, top, board)
                pygame.display.update()
                HOVER_COLOR = Temp # changing HOVER_COLOR back to previous value
                pygame.time.wait(1000)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        #PrintChance(chance)
        DrawBoard(board) # Draw Board..
        if MouseCollideSomeBox(mousex, mousey, board): # Actually not collide...
            #...just if mouse is over some box.
            DrawHoverBox(mousex, mousey, board) # draw hover box over it.
            
        if mouseClicked:
            print 'chance:',chance
            #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            print OurRow, OurCol
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if MouseCollideOurBox(mousex, mousey, board,OurRow, OurCol):
                
                GameWonAnimation()
                pygame.time.wait(2000)
                START_BUTTON_ON = False
                chance+=1
            elif MouseCollideSomeBox(mousex, mousey, board):
                chance+=1
                PrintChance(chance)
                if chance >= 6:
                    GameOverAnimation()
                    pygame.time.wait(2000)
                    START_BUTTON_ON = False
                    break
        pygame.display.update()
'''
#Main game loop
for turn in range(3): #Loop executes 3 times to give 3 chances to the user
    print "------"*10 ,
    print "Chance number:",(turn+1) #Prints chance number
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    
    if guess_row == ship_row and guess_col == ship_col: #Battle won!!
        print "~*~*~*~*"*10
        print "Congratulations! You sunk my battleship!"
        print "~*~*~*~*"*10
        break
    
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4): #When guess out of range
            print "~~~~~"*10
            print "Oops, that's not even in the ocean."
            print "~~~~~"*10
            if turn==3:
                print "|~~~~~~  Game Over  ~~~~~~|"
        elif(board[guess_row][guess_col] == "X"): #When guess is same as the last one
            print "~~~~~"*10
            print "You guessed that one already."
            print "~~~~~"*10
            if turn==3:
                print "|~~~~~~  Game Over  ~~~~~~|"
        else: #When guess is wrong
            print "~~~~~"*10
            print "You missed my battleship!"
            print "~~~~~"*10
            board[guess_row][guess_col] = "X"
            print_board(board)
            if turn==3:
                print "|~~~~~~  Game Over  ~~~~~~|"

#Program will wait for 5 seconds before halting
time.sleep(5)

'''

