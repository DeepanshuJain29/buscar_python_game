import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~
SEL_BOX_LIST = [] # List of selected boxes.
SCR_HEIGHT = 680
SCR_WIDTH = 600
BOARD_HEIGHT = 5 # number of rows in board
BOARD_WIDTH = 5 # number of columns in board
#SEL_BOXSIZE = 70 # length and breadth of selected box
BOXSIZE = 80 # length and breadth of box
GAPSIZE = 5 # gap b/w boxes
START_FONT_SIZE = 50 # Font size for 'StartButton' text
#-------------- DISPLAY -----------------------------------------
Display = pygame.display.Info()
DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Battleship')
#----------------------------------------------------------------
#----COLORS------
BOX_COLOR = (255,0,0)
START_COLOR = (0, 0, 255)
SEL_BOX_COLOR = (0, 0, 255)
BGCOLOR = (255, 255, 255, 120)
BGCOLOR = (255, 255, 255) 
GREEN = (0,255,0)
BLUE = (0,0,255)
HOVER_COLOR = (41,41,41)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#----------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    
def DrawBoard(board, SEL_BOX_LIST): # drawing board
    for row in board:
        for box in row:
            left,top = LeftTopOf(box, board)
            ThisBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if ThisBox in SEL_BOX_LIST:
                pygame.draw.rect(DISPLAYSURF,SEL_BOX_COLOR,(left,top,BOXSIZE, BOXSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOXSIZE, BOXSIZE))

def DrawStartButton(x = False): # Do not draw button unless x is given true.
    # Placing start button.
    top = (SCR_WIDTH/2)-100
    left = SCR_HEIGHT/2-40
    StartButton = pygame.Rect(top,left, 200, 80)
    if not x: # when x is false give StartButton's rect.
        return StartButton
    else: # otherwise draw it
        for x in range(255): # Start button fade-in.
            pygame.time.wait(1)
            START_COLOR = (255-x,255-x,255)
            pygame.draw.rect(DISPLAYSURF, WHITE, StartButton)
            pygame.draw.rect(DISPLAYSURF, START_COLOR, StartButton)
            FontObj_Start = pygame.font.Font('PoplarStd.otf', START_FONT_SIZE)
            StartButtonText = FontObj_Start.render('START', True, WHITE, START_COLOR)
            StartButtonText_Rect = StartButtonText.get_rect()
            StartButtonText_Rect.center = StartButton.center
            DISPLAYSURF.blit(StartButtonText, StartButtonText_Rect)
            pygame.display.update()

def IntroAnimation(x = False): # Animation played when game is started.
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
    pygame.time.wait(80) # Wait for some time...
    for pos in range(SCR_HEIGHT/2,SCR_HEIGHT/2-100,-1): # 3rd animation, to bring the...
        #....text some coordinates up making space for 'start button'.
        LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, pos)
        pygame.draw.rect(DISPLAYSURF, WHITE, (270,0, 100, SCR_HEIGHT/2))
        DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
        pygame.display.update() # update screen after each loop

def RandomRow(board):
    return randint(1, len(board))

def RandomCol(board):
    return randint(1, len(board[0]))

def MouseHoverSomeBox (mousex, mousey, board): # check if mouse was hovered...
    #...over any box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(box, board)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                return True 

    

def MouseCollideSomeBox(mousex, mousey, board): # check if mouse collided...
    #...with any box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(box, board)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox in SEL_BOX_LIST: # If clicked selected box, don't do anything...
                pass
            else: # otherwise return True.
                if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                    SEL_BOX_LIST.append(AnyBox) # then append it into SEL_BOX_LIST.
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
                if AnyBox in SEL_BOX_LIST: # If hovered over selected box, don't do anything...
                    pass
                else: # otherwise Draw hover box.
                    pygame.draw.rect(DISPLAYSURF, HOVER_COLOR, (left, top, BOXSIZE, BOXSIZE))
                    pygame.display.update()
                return None # just to stop the box loop and row loop.

def GameOverAnimation():
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(33):        
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(BLACK)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
    #-----------------------------------------------------------------------------
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
    del SEL_BOX_LIST [:] # Empty SEL_BOXL_IIST when game is over..
    
def GameWonAnimation():
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(33):        
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(WHITE)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
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
    for alpha in range(33):
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(GREEN)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
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
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(33, 0, -1):
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(BGCOLOR)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
    #-----------------------------------------------------------------------------
    #DISPLAYSURF.fill(BGCOLOR)
    #pygame.display.update()

def Enter_TextAnimation():
    ENTER_TEXTSIZE = 20
    FontObj_1 = pygame.font.Font('freesansbold.ttf', ENTER_TEXTSIZE)
    for BlueVal in range(255):
        BLUE = (0, 0, BlueVal) 
        EnterText = FontObj_1.render("Press 'ENTER' or Click on 'START' to Start the game", True, BLUE)
        EnterText_Rect = EnterText.get_rect()
        EnterText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2+150)
        DISPLAYSURF.blit(EnterText, EnterText_Rect)
        pygame.display.update()
    pygame.time.wait(100)
    for BlueVal in range(255):
        BLUE = (BlueVal, BlueVal, BlueVal) 
        EnterText = FontObj_1.render("Press 'ENTER' or Click on 'START' to Start the game", True, BLUE)
        EnterText_Rect = EnterText.get_rect()
        EnterText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2+150)
        DISPLAYSURF.blit(EnterText, EnterText_Rect)
        pygame.display.update()


board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.

while True: # Main Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    OurRow = RandomRow(board)
    OurCol = RandomCol(board)
    START_BUTTON_ON = False # Initially StartButton is 'OFF'
    chance = 1
    if not START_BUTTON_ON: # Animate intro animation if START_BUTTON is not 'ON'
        DISPLAYSURF.fill(BGCOLOR) # Coloring the window background 
        #----------------Starting intro animation---------
        IntroAnimation() # Invoking IntroAnimation
        DrawStartButton(True)
        pygame.display.update()
        #-------------------------------------------------
    mousex = 0
    mousey = 0
    while not START_BUTTON_ON: # Loop unless Start Button is clicked.
        #Enter_TextAnimation()
        StartButton_Rect = DrawStartButton()
        for event in pygame.event.get(): # Checking each event happening on window.
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP: # If button was clicked..
                mousex, mousey = event.pos
                if StartButton_Rect.collidepoint(mousex, mousey): #..check if StartButton..
                    #...was clicked
                    START_BUTTON_ON = True # Now Start Button is 'ON'
    while START_BUTTON_ON: # Finally Start Button is clicked (or, it is 'ON').
        mouseClicked = False
        #~~~ ****** ~~~~~~~ ****** ~~~~~~~~ ****** ~~~~~~~ ****** ~~~~~~~~
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            elif (event.type == KEYDOWN and event.key == K_a):
                left = OurCol * (BOXSIZE + GAPSIZE)+30 
                top = OurRow * (BOXSIZE + GAPSIZE)+30
                Temp = HOVER_COLOR # Storing HOVER_COLOR in temporary variable
                HOVER_COLOR = (200,0,0) # changing HOVER_COLOR(a bit light).
                DrawHoverBox(left, top, board)
                HOVER_COLOR = Temp # changing HOVER_COLOR back to previous value
                pygame.time.wait(60)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                    mousex, mousey = event.pos
                    mouseClicked = True
        #~~~ ****** ~~~~~~~ ****** ~~~~~~~~ ****** ~~~~~~~ ****** ~~~~~~~~
        DISPLAYSURF.fill(BGCOLOR)
        DrawBoard(board, SEL_BOX_LIST) # Draw Board..
        if MouseHoverSomeBox(mousex, mousey, board): # if mouse hovers over some box.
            DrawHoverBox(mousex, mousey, board) # draw hover box over it.   
        if mouseClicked:
            print 'chance:',chance
            #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            print OurRow, OurCol
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if MouseCollideOurBox(mousex, mousey, board,OurRow, OurCol):
                GameWonAnimation()
                pygame.time.wait(1500)
                START_BUTTON_ON = False
            elif MouseCollideSomeBox(mousex, mousey, board):
                pygame.time.wait(200)
                if chance == 5:
                    GameOverAnimation()
                    pygame.time.wait(2000)
                    START_BUTTON_ON = False
                    break
                chance+=1
                PrintChance(chance)
        pygame.display.update()

