import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~
#-------------- DISPLAY -----------------------------------------
Display = pygame.display.Info()
SCR_HEIGHT = Display.current_h
SCR_WIDTH = Display.current_w
DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Battleship')
#----------------------------------------------------------------
SEL_BOX_LIST = [] # List of selected boxes.
BOARD_HEIGHT = 4 # number of rows in board
BOARD_WIDTH = 4 # number of columns in board
#SEL_BOXSIZE = 70 # length and breadth of selected box
BOXSIZE = 50 # length and breadth of box
GAPSIZE = 5 # gap b/w boxes
START_FONT_SIZE = 50 # Font size for 'StartButton' text
INSTRUC_FONT_SIZE = 20 # Font size for 'InstrucButton' text
XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
OUR_BOXES = [] # List of boxes which have Battleship under it. [contains (row, col) tuple]
#----COLORS------
WIN_BOX_COLOR = (255, 255, 255) # color for box which contains Battleship...
#...(appears only after clicking on it)
BOX_COLOR = (255,0,0)
START_COLOR = (0, 0, 255)
INSTRUC_COLOR = (0, 0, 0)
BGCOLOR = (30, 30, 30) 
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

def LeftTopOf(board, box = 0, BoxRowColTup = 0):#getting left top coordinates of a box in board
    # left top coordinates can be fetched in two ways, one is to give the...
    #...box number [like: 2,3,4..(refer to "Example of board.." above.)]...
    #...and another way is to give (row, col) tuple...
    #...BoxRowColTup does the same.
    #...so either you give 'BoxRowColTup' or 'box' number.
    if type(BoxRowColTup) == tuple: # check if BoxRowColTup is given in tuplle form.
        row, col = BoxRowColTup
        left = ((col * (BOXSIZE + GAPSIZE)) - (BOXSIZE + GAPSIZE)) + XMARGIN
        top = ((row * (BOXSIZE + GAPSIZE)) - (BOXSIZE + GAPSIZE)) + YMARGIN
        return (left, top)
    else:# otherwise confirm that box number is given.
        boxRow , boxCol = RowColOf(box,board)    
        left = ((boxCol * (BOXSIZE + GAPSIZE)) - (BOXSIZE + GAPSIZE)) + XMARGIN
        top = ((boxRow * (BOXSIZE + GAPSIZE)) - (BOXSIZE + GAPSIZE)) + YMARGIN
        return (left,top)            
    
def DrawBoard(board, SEL_BOX_LIST, x = 'default'): # drawing board
    # first we convert above defined OUR_BOXES list into...
    #...rect form (as it contains (row, col) tuple).
    OUR_BOXES_RECT = [] # here is the list to contain rect(s).
    for each in OUR_BOXES:
        left, top = LeftTopOf(board, BoxRowColTup = each)
        BoxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        OUR_BOXES_RECT.append(BoxRect)
    if x == 'default': # Check if x is not given any value, if yes, then draw normal board.
        for row in board: # in row
            for box in row: # on box
                left,top = LeftTopOf(board, box)
                ThisBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if ThisBox in SEL_BOX_LIST: # first se that if ThisBox is in SEL_BOX_LIST.
                    if ThisBox in OUR_BOXES_RECT: # next check if it is also one of the...
                        #...box to contain Battleship, if so, then paint it with WIN_BOX_COLOR.
                        pygame.draw.rect(DISPLAYSURF,WIN_BOX_COLOR,(left,top,BOXSIZE, BOXSIZE))
                    else: # otherwise paint it with BGCOLOR.
                        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE, BOXSIZE))                        
                else: # otherwise paint it normally (with BOX_COLOR).
                    pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOXSIZE, BOXSIZE))
    elif x == 'start':# otherwise, draw it with animation (it means board is drawn first time).
        for row in board:
            for box in row:
                left,top = LeftTopOf(board, box)
                pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOXSIZE, BOXSIZE))
                pygame.display.update()
                pygame.time.wait(90)
                
def ReturnToHome(x = False): # Draw Retu
    COLOR = (100, 100, 100)
    FONT_SIZE = 30
    PointsX = (100)
    PointsY = (SCR_HEIGHT-50)
    PointsXY = (PointsX, PointsY)
    if not x:
        return pygame.Rect(PointsX,PointsY-20, 210, 40)
    elif x:
        Coordinates = (PointsXY, (PointsX+25, PointsY-20), (PointsX+25, PointsY+20))
        pygame.draw.polygon(DISPLAYSURF, COLOR, Coordinates)
        FontObj = pygame.font.Font('PoplarStd.otf', FONT_SIZE)
        RTHText = FontObj.render('RETURN TO MENU', True, COLOR, BGCOLOR)
        RTHText_Rect = RTHText.get_rect()
        RTHText_Rect.center = (PointsX+120, PointsY+5)
        DISPLAYSURF.blit(RTHText, RTHText_Rect)
    
            
def DrawStartButton(x = False): # Do not draw button unless x is given true.
    # Placing start button.
    left = SCR_WIDTH/2
    top = SCR_HEIGHT/2 + 30
    StartButton = pygame.Rect(left-100,top-40, 200, 80)
    if not x: # when x is false give StartButton's rect.
        return StartButton
    else: # otherwise draw it
        for size in range(25): # First animation. (Of resizing start button's background)
            #--------------------- TOP - LEFT of surface (which enlarge during the loop)-----
            left = SCR_WIDTH/2
            top = SCR_HEIGHT/2 + 30
            #--------------------------------------------------------------------------------
            #pygame.time.wait(10)
            width = 200 + size # Width of surface increases after every loop...
            height = 80 + size #...and same for height
            BG = pygame.Surface((width, height))
            BG.fill((0,0,0))
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size -
            top = top - (height/2)
            DISPLAYSURF.blit(BG, (left,top))
            #------------------------- Drawing Start Button --------------
            START_COLOR = (255,0,0)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, StartButton)
            pygame.draw.rect(DISPLAYSURF, START_COLOR, StartButton)
            FontObj_Start = pygame.font.Font('PoplarStd.otf', START_FONT_SIZE)
            StartButtonText = FontObj_Start.render('START', True, WHITE, START_COLOR)
            StartButtonText_Rect = StartButtonText.get_rect()
            StartButtonText_Rect.center = StartButton.center
            DISPLAYSURF.blit(StartButtonText, StartButtonText_Rect)
            pygame.display.update()
            #--------------------------------------------------------------
        for size in range(25): # Second animation. (Of hiding the enlarged background)
            #--------------------- TOP - LEFT of surface (which enlarge during the loop)-----
            left = SCR_WIDTH/2
            top = SCR_HEIGHT/2 + 30
            #--------------------------------------------------------------------------------
            #pygame.time.wait(10)
            width = 200 + size # Width of surface increases after every loop...
            height = 80 + size #...and same for height
            BG = pygame.Surface((width, height))
            BG.fill(BGCOLOR)
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size -
            top = top - (height/2)
            DISPLAYSURF.blit(BG, (left,top))
            #------------------------- Drawing Start Button --------------
            START_COLOR = (255,0,0)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, StartButton)
            pygame.draw.rect(DISPLAYSURF, START_COLOR, StartButton)
            FontObj_Start = pygame.font.Font('PoplarStd.otf', START_FONT_SIZE)
            StartButtonText = FontObj_Start.render('START', True, WHITE, START_COLOR)
            StartButtonText_Rect = StartButtonText.get_rect()
            StartButtonText_Rect.center = StartButton.center
            DISPLAYSURF.blit(StartButtonText, StartButtonText_Rect)
            pygame.display.update()
            #--------------------------------------------------------------

def DrawInstrucButton(x = False): # Do not draw button unless x is given true.
    # Placing start button.
    left = SCR_WIDTH/2
    top = SCR_HEIGHT/2 + 140
    InstrucButton = pygame.Rect(left-70,top-30, 140, 60)
    if not x: # when x is false give InstrucButton's rect.
        return InstrucButton
    elif x == 'hover': # if x  = 'hover' then draw hover box.
        for size in range(25): # First animation. (Of resizing start button's background)
            #--------------------- TOP - LEFT of surface (which enlarge during the loop)-----
            left = SCR_WIDTH/2
            top = SCR_HEIGHT/2 + 140
            #--------------------------------------------------------------------------------
            width = 130 + size # Width of surface increases after every loop...
            height = 50 + size #...and same for height
            BG = pygame.Surface((width, height))
            BG.fill((0,0,0))
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size -
            top = top - (height/2)
            DISPLAYSURF.blit(BG, (left,top))
            #------------------------- Drawing Instruc Button --------------
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, InstrucButton)
            pygame.draw.rect(DISPLAYSURF, INSTRUC_COLOR, InstrucButton)
            FontObj_Instruc = pygame.font.Font('PoplarStd.otf', INSTRUC_FONT_SIZE)
            InstrucButtonText = FontObj_Instruc.render('INSTRUCTIONS', True, WHITE, INSTRUC_COLOR)
            InstrucButtonText_Rect = InstrucButtonText.get_rect()
            InstrucButtonText_Rect.center = InstrucButton.center
            DISPLAYSURF.blit(InstrucButtonText, InstrucButtonText_Rect)
            pygame.display.update()
            #--------------------------------------------------------------
        for size in range(25): # First animation. (Of resizing start button's background)
            #--------------------- TOP - LEFT of surface (which enlarge during the loop)-----
            left = SCR_WIDTH/2
            top = SCR_HEIGHT/2 + 140
            #--------------------------------------------------------------------------------
            #pygame.time.wait(10)
            width = 130 + size # Width of surface increases after every loop...
            height = 50 + size #...and same for height
            BG = pygame.Surface((width, height))
            BG.fill(BGCOLOR)
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size -
            top = top - (height/2)
            DISPLAYSURF.blit(BG, (left,top))
            #------------------------- Drawing Instruc Button --------------
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, InstrucButton)
            pygame.draw.rect(DISPLAYSURF, INSTRUC_COLOR, InstrucButton)
            FontObj_Instruc = pygame.font.Font('PoplarStd.otf', INSTRUC_FONT_SIZE)
            InstrucButtonText = FontObj_Instruc.render('INSTRUCTIONS', True, WHITE, INSTRUC_COLOR)
            InstrucButtonText_Rect = InstrucButtonText.get_rect()
            InstrucButtonText_Rect.center = InstrucButton.center
            DISPLAYSURF.blit(InstrucButtonText, InstrucButtonText_Rect)
            pygame.display.update()
            #--------------------------------------------------------------
    elif x: # when x is given True, draw it.
        left = SCR_WIDTH/2
        top = SCR_HEIGHT/2 + 140
        #------------------------- Drawing Instruc Button --------------
        START_COLOR = (0,0,0)
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, InstrucButton)
        pygame.draw.rect(DISPLAYSURF, INSTRUC_COLOR, InstrucButton)
        FontObj_Instruc = pygame.font.Font('PoplarStd.otf', INSTRUC_FONT_SIZE)
        InstrucButtonText = FontObj_Instruc.render('INSTRUCTIONS', True, WHITE, INSTRUC_COLOR)
        InstrucButtonText_Rect = InstrucButtonText.get_rect()
        InstrucButtonText_Rect.center = InstrucButton.center
        DISPLAYSURF.blit(InstrucButtonText, InstrucButtonText_Rect)
        pygame.display.update()
        #--------------------------------------------------------------

def Enter_Text(): # write the text - "Press 'ENTER' or Click on 'START' to Start the game".
    ENTER_TEXTSIZE = 20
    FontObj_1 = pygame.font.Font('freesansbold.ttf', ENTER_TEXTSIZE)
    COLOR = (5, 5, 5) 
    EnterText = FontObj_1.render("Press 'ENTER' or Click on 'START' to Start the game", True, COLOR, BGCOLOR)
    EnterText_Rect = EnterText.get_rect()
    EnterText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT-150)
    DISPLAYSURF.blit(EnterText, EnterText_Rect)
    pygame.display.update()

def IntroPage(): # Page shown when game is started.
    INTRO_FONT_SIZE = 100 # Font size for 'Battleship' text
    FontObj = pygame.font.Font('gomarice_kaiju_monster.ttf', INTRO_FONT_SIZE)        
    LetsPlayBattleship = FontObj.render("Battleship!", True, GREEN, BGCOLOR)
    LetsPlayBattleship_Rect = LetsPlayBattleship.get_rect()
    LetsPlayBattleship_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2-90)
    DISPLAYSURF.blit(LetsPlayBattleship, LetsPlayBattleship_Rect)
    pygame.display.update()
    #---------------------- Finally Drawing buttons and Enter text. ----
    DrawInstrucButton(True)
    DrawStartButton(True)
    Enter_Text()
    #-------------------------------------------------------------------

def DrawInstrucBox(x = 'ON'): # screen drawn when user clicks on Instructions button.
    if x == 'ON': # when x is 'ON', fade (the screen) in and display instructions.
        # Transparent Overlay Animation ----------------------------------------------
        for alpha in range(28):
            Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
            Overlay.set_alpha(alpha)                # alpha level
            Overlay.fill(RED)           # this fills the entire surface
            DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
            pygame.display.update()
        #-----------------------------------------------------------------------------
        # And finally here is the png image of instructions.
        TextImage = pygame.image.load('Instructions.png')
        DISPLAYSURF.blit(TextImage, (SCR_WIDTH/2-400,60))
        pygame.display.update()
    elif x == 'OFF': # when x is given 'OFF' fill the screen with BGCOLOR, and show 'IntroPage'.
        DISPLAYSURF.fill(BGCOLOR)
        IntroPage()           

def RandomRow(board): # to generate random row.
    return randint(1, len(board))

def RandomCol(board): # to generate random column.
    return randint(1, len(board[0]))

def RandomBoxes(board, level): # here we combine RandomRow and RandomCol in a tuple...
    #...and append it into OUR_BOXES, it will generate RandomBoxes on the basis of 'level'.
    for n in range(level): # iterate 'level' times.
        row = RandomRow(board)
        col = RandomCol(board)
        box = (row, col)
        while box in OUR_BOXES:
            row = RandomRow(board)
            col = RandomCol(board)
            box = (row, col)
        OUR_BOXES.append((row, col))
    return OUR_BOXES

def MouseHoverSomeBox (mousex, mousey, board): # check if mouse was hovered...
    #...over any box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(board, box)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                return True 

    

def MouseCollideSomeBox(mousex, mousey, board): # check if mouse collided...
    #...with any box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(board, box)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox in SEL_BOX_LIST: # If clicked selected box, don't do anything...
                pass
            else: # otherwise return True.
                if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with AnyBox
                    SEL_BOX_LIST.append(AnyBox) # then append it into SEL_BOX_LIST.
                    return True 

def MouseCollideOurBox(mousex, mousey, board, OurBoxes): # check if mouse collided...
    #...with our box.
    for row in board: # each row
        for box in row: # each box
            left,top = LeftTopOf(board, box)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox.collidepoint(mousex, mousey): # check if mouse collided with any box
                if RowColOf(box, board) in OurBoxes: # now check if box was one of our boxes.
                    SEL_BOX_LIST.append(AnyBox) # then append it into SEL_BOX_LIST.
                    return True                



def DrawHoverBox(mousex, mousey, board):#Draw hover box over a box viz. under mouse coordinates
    for row in board:
        for box in row:
            left,top = LeftTopOf(board, box)
            AnyBox = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if AnyBox.collidepoint(mousex, mousey): # if we come up with our box..
                #...draw hover box over it.
                if AnyBox in SEL_BOX_LIST: # If hovered over selected box, don't do anything...
                    pass
                else: # otherwise Draw hover box.
                    pygame.draw.rect(DISPLAYSURF, HOVER_COLOR, (left, top, BOXSIZE, BOXSIZE))
                    pygame.display.update()
                return None # just to stop the box loop and row loop.

def GameOverAnimation(): # screen to draw Game Over Animation.
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
    del SEL_BOX_LIST [:] # Empty SEL_BOXL_IIST and OUR_BOXES list when game is over..
    del OUR_BOXES[:]
    
def GameWonAnimation(): # screen to draw Game Won Animation.
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(30):        
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(RED)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
    #-----------------------------------------------------------------------------
    GAME_WON_SIZE = 90 # Font size for 'GameOver' text
    FontObj_Over = pygame.font.Font('PoplarStd.otf', GAME_WON_SIZE)
    GameWonText = FontObj_Over.render('YOU WON', True, WHITE)
    GameWonText_Rect = GameWonText.get_rect()
    GameWonText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2)
    DISPLAYSURF.blit(GameWonText, GameWonText_Rect)
    pygame.display.update()
    del SEL_BOX_LIST [:] # Empty SEL_BOX_IIST and OUR_BOXES list when game is won..
    del OUR_BOXES[:]
    pygame.time.wait(800)

def PrintChance(x): # Prints the chance.
    CHANCE_SIZE = 50 # Font size for 'GameOver' text
    FontObj_Chance = pygame.font.Font('SHOWG.ttf', CHANCE_SIZE)
    ChanceText = FontObj_Chance.render('CHANCE :'+str(x), True, WHITE)
    ChanceText_Rect = ChanceText.get_rect()
    ChanceText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT - 50)
    DISPLAYSURF.blit(ChanceText, ChanceText_Rect)

def GameOver(board): # check if Game(is)Over. (it goes through each box in OUR_BOXES...
    #...and checks if it is present in SEL_BOX_LIST, if all of them are in SEL_BOX_LIST...
    #...then GameOver, otherwise carry on.)
    for box in OUR_BOXES:
        left, top = LeftTopOf(board, BoxRowColTup = box)
        BoxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        if BoxRect not in SEL_BOX_LIST:
            return False
    return True

assert BOARD_WIDTH == BOARD_HEIGHT # Board needs to have an equal number of boxes.
board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.

while True: # Main Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    DISPLAYSURF.fill(BGCOLOR)
    START_BUTTON_ON = False # Initially StartButton is 'OFF'.
    if not START_BUTTON_ON: # Show IntroPage if START_BUTTON is not 'ON'
        DISPLAYSURF.fill(BGCOLOR) # Coloring the window background 
        #---------------- Displaying IntroPage ---------
        IntroPage() # Drawing Intro page
        pygame.display.update()
        #-------------------------------------------------
    mousex = 0 # initially storing mouse's x and y in these variables.
    mousey = 0
    while not START_BUTTON_ON: # Loop unless Start Button is clicked.
        IntroPage() # Drawing Intro page
        INSTRUC_BOX = 'OFF' # Initially InstrucBox isn't displayed.
        InstrucButton_Rect = DrawInstrucButton() # Now getting Instruc and Start buttons' rect.
        StartButton_Rect = DrawStartButton()
        # Now check if mouse is on Instruc Button -------------------------
        if InstrucButton_Rect.collidepoint(mousex, mousey):
            while InstrucButton_Rect.collidepoint(mousex, mousey): # draw hovered Instruc...
                #...Button until mouse is on it.
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP: # If button was clicked..
                        mousex, mousey = event.pos
                        if InstrucButton_Rect.collidepoint(mousex, mousey): #..check if..
                            #..InstrucButton was clicked
                            DrawInstrucBox() # then DrawInstrucBox...
                            INSTRUC_BOX = 'ON' #...and switch 'ON' INSTRUC_BOX.
                            while INSTRUC_BOX == 'ON': # now, until INSTRUC_BOX is 'ON'...
                                #...check just for a mouse click...
                                for event in pygame.event.get(): # Checking each event...
                                    #...happening on window.
                                    if event.type == MOUSEBUTTONUP: # If mouse was clicked...
                                        #...switch 'OFF' INSTRUC_BOX.
                                        INSTRUC_BOX = 'OFF'
                                        DrawInstrucBox('OFF')
                                        mousex = 0
                                        mousey = 0
                DrawInstrucButton('hover') # Drawing hover version of Instruc Button.
        #--------------------------------------------------------------------
        for event in pygame.event.get(): # Checking each event happening on window.
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == KEYUP and event.key == K_RETURN: # If Enter was pressed.
                START_BUTTON_ON = True # Now Start Button is 'ON'
            elif event.type == MOUSEBUTTONUP: # If button was clicked..
                mousex, mousey = event.pos
                if StartButton_Rect.collidepoint(mousex, mousey): #..check if StartButton..
                    #...was clicked
                    START_BUTTON_ON = True # Now Start Button is 'ON'
    #---------------------------- INITIALS -----------------
    found = 0
    level = 1
    OurBoxes = RandomBoxes(board, level)    
    chance = 1
    BGCOLOR = (30, 30, 30)
    BOX_COLOR =(255, 0, 0)
    DISPLAYSURF.fill(BGCOLOR)
    board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
    DrawBoard(board, SEL_BOX_LIST, 'start') # Draw Board.
    #------------------------------------------------------------------------
    while START_BUTTON_ON: # Finally Start Button is clicked (or, it is 'ON').
        # redefining X and Y MARGINs, just because BOARDs WIDTH is changed after each level.
        if BOARD_WIDTH == 26 : # When board is full.
            START_BUTTON_ON = False
            BOARD_HEIGHT = 4
            BOARD_WIDTH = 4
            XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
            YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
            BGCOLOR = (30, 30, 30)
            break
        XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
        YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
        ReturnToHome_Rect = ReturnToHome()
        mouseClicked = False # Initially mouse isn't Clicked.
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                    mousex, mousey = event.pos
                    mouseClicked = True
        #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            elif (event.type == KEYUP and event.key == K_a):
                for each in OUR_BOXES:
                    row, col = each
                    left = (col * (BOXSIZE + GAPSIZE) - (BOXSIZE + GAPSIZE)) + XMARGIN
                    top = (row * (BOXSIZE + GAPSIZE) - (BOXSIZE + GAPSIZE)) + YMARGIN
                    Temp = HOVER_COLOR # Storing HOVER_COLOR in temporary variable
                    HOVER_COLOR = (200,0,0) # changing HOVER_COLOR(a bit light).
                    DrawHoverBox(left, top, board)
                    HOVER_COLOR = Temp # changing HOVER_COLOR back to previous value
                pygame.time.wait(100)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #--- Drawing - board (again, but without Animation), ReturnToHome and PrintChance -----
        DISPLAYSURF.fill(BGCOLOR)
        ReturnToHome(True)
        PrintChance(chance)
        board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
        DrawBoard(board, SEL_BOX_LIST)
        #---------------------------------------------------------------------
        if MouseHoverSomeBox(mousex, mousey, board): # if mouse hovers over some box.
            DrawHoverBox(mousex, mousey, board) # draw hover box over it.   
        if mouseClicked:
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print 'CHANCE:',chance
            #~~~~~~~~~~~~~~CHEAT~~~~~~~~~~~~~
            print OurBoxes
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if ReturnToHome_Rect.collidepoint(mousex, mousey):
                START_BUTTON_ON = False
                del SEL_BOX_LIST[:]
                del OUR_BOXES[:]
                BOARD_WIDTH = 4 # return BOARD's WIDTH and HEIGHT back to 4...
                BOARD_HEIGHT = 4
                #...X and Y MARGIN back to its original value...
                XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                BGCOLOR = (30, 30, 30) #...and BGOLOR to its original value.
            elif MouseCollideOurBox(mousex, mousey, board,OurBoxes): # If mouse was...
                #...clicked on our box...
                if not GameOver(board):
                    pass
                else:
                    GameWonAnimation()#...Display GameWonAnimation.
                    level+=1
                    RR = randint(0,100)
                    RG = randint(0,100)
                    RB = randint(0,100)
                    BGCOLOR = (RR, RG, RB)
                    RR = randint(100,255)
                    RG = randint(100,255)
                    RB = randint(100,255)
                    BOX_COLOR = (RR, RG, RB)
                    if BOARD_WIDTH <= 6 or BOARD_HEIGHT > 8:
                        BOARD_WIDTH  += 2 # Increase the BOARD's WIDTH.
                        #--------------------------- And the same process ------------
                        OurBoxes = RandomBoxes(board, level)
                        board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
                        DISPLAYSURF.fill(BGCOLOR)
                        DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                        #-------------------------------------------------------------
                    elif BOARD_WIDTH >6 and  BOARD_HEIGHT <=8:
                        BOARD_HEIGHT  += 2 # Increase the BOARD's WIDTH.
                        #--------------------------- And the same process ------------
                        OurBoxes = RandomBoxes(board, level)
                        board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
                        DISPLAYSURF.fill(BGCOLOR)
                        DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                        #-------------------------------------------------------------
                    found = 0
            elif MouseCollideSomeBox(mousex, mousey, board):# If mouse was...
                #...clicked on any box...
                #pygame.time.wait(200)
                if chance == 5: #...and if chances are 5 (Finally..)...
                    GameOverAnimation() #...display GameOverAnimation. 
                    BOARD_WIDTH = 4 # return BOARD's WIDTH and HEIGHT back to 4...
                    BOARD_HEIGHT = 4
                    #...X and Y MARGIN back to its original value...
                    XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                    YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                    BGCOLOR = (30, 30, 30) #...and BGOLOR to its original value.
                    pygame.time.wait(2000)
                    START_BUTTON_ON = False
                    break
                chance+=1 # Increase the chances.
        pygame.display.update()
