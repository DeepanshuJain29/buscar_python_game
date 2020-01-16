import pygame, sys, time, os
from pygame.locals import *
from random import randint

# just to calculate the screen's dimensions ---------------------------------------------------------
pygame.init()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~~~~~
#-------------- DISPLAY -----------------------------------------
Display = pygame.display.Info()
SCR_HEIGHT = Display.current_h
SCR_WIDTH = Display.current_w
DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.FULLSCREEN)
pygame.display.quit()
pygame.display.set_caption('Buscar')
#----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

START = False
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
OUR_BOXES = [] # List of boxes which have hidden thing under it. [contains (row, col) tuple]
#----COLORS------
WIN_BOX_COLOR = (255, 255, 255) # color for box which contains hidden thing...
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#--------------------------------------------------------------------- FUNCTIONS --------------
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

# Example of Board --- Here is board of height 2 and width 4 ---- [[1, 2, 3, 4], [5, 6, 7, 8]]

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
                        #...box to contain hidden thing, if so, then paint it with WIN_BOX_COLOR.
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
                
def ReturnToHome(x = False): # Draw ReturnToHome button.
    FONT_SIZE = 30
    PointsX = (100)
    PointsY = (SCR_HEIGHT-50)
    PointsXY = (PointsX, PointsY)
    if not x: # just return its rect if x is False..
        return pygame.Rect(PointsX,PointsY-20, 210, 40)
    elif x: #..otherwise draw it.
        Coordinates = (PointsXY, (PointsX+25, PointsY-20), (PointsX+25, PointsY+20))
        pygame.draw.polygon(DISPLAYSURF, WHITE, Coordinates)
        FontObj = pygame.font.Font('PoplarStd.otf', FONT_SIZE)
        RTHText = FontObj.render('RETURN TO MENU', True, WHITE, BGCOLOR)
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
    # Placing Instruc button.
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
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size -----
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
        for size in range(25): # Second animation. (Of erasing previously drawn background)
            #--------------------- TOP - LEFT of surface (which enlarge during the loop)-----
            left = SCR_WIDTH/2
            top = SCR_HEIGHT/2 + 140
            #--------------------------------------------------------------------------------
            width = 130 + size # Width of surface increases after every loop...
            height = 50 + size #...and same for height
            BG = pygame.Surface((width, height))
            BG.fill(BGCOLOR)
            left = left - (width/2) #------ Here TOP - LEFT are adjusting with increase in size ----
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
    elif x: # when x is given True, just draw it.
        left = SCR_WIDTH/2
        top = SCR_HEIGHT/2 + 140
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
    INTRO_FONT_SIZE = 100 # Font size for 'Buscar' text
    FontObj = pygame.font.Font('gomarice_kaiju_monster.ttf', INTRO_FONT_SIZE)        
    Buscar = FontObj.render("Buscar!", True, GREEN, BGCOLOR)
    Buscar_Rect = Buscar.get_rect()
    Buscar_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2-90)
    DISPLAYSURF.blit(Buscar, Buscar_Rect)
    pygame.display.update()
    #---------------------- Finally drawing buttons and Enter text. ----
    DrawInstrucButton(True)
    DrawStartButton(True)
    Enter_Text()
    #-------------------------------------------------------------------

def DrawInstrucBox(x = 'ON'): # screen drawn when user clicks on Instructions button.
    if x == 'ON': # when x is 'ON', fade (the screen) in and display instructions.
        # Transparent Overlay Animation ----------------------------------------------
        for alpha in range(100):
            Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
            Overlay.set_alpha(alpha)                # alpha level
            Overlay.fill(RED)           # this fills the entire surface
            DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
            pygame.display.update()
        
        #-----------------------------------------------------------------------------
        # And finally here is the png image of instructions.
        TextImage = pygame.image.load('Instructions.png')
        DISPLAYSURF.blit(TextImage, (SCR_WIDTH/2-470,SCR_HEIGHT/2-400))
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
    for n in range(level+2): # iterate 'level' times.
        row = RandomRow(board)
        col = RandomCol(board)
        box = (row, col)
        while box in OUR_BOXES: # just to ensure that row and column does not repeat.
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



def DrawHoverBox(mousex, mousey, board):# Draw hover box over a box which is under mouse coordinates
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
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of our rect
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
    del SEL_BOX_LIST [:] # Empty SEL_BOX_LIST and OUR_BOXES list when game is over..
    del OUR_BOXES[:]
    
def GameWonAnimation(): # screen to draw Game Won Animation.
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(30):        
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of our rect
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
    pygame.time.wait(400)

def PrintChance(x): # Prints the chance.
    CHANCE_SIZE = 50 # Font size for 'PrintChance' text
    FontObj_Chance = pygame.font.Font('SHOWG.ttf', CHANCE_SIZE)
    ChanceText = FontObj_Chance.render('CHANCE :'+str(x), True, WHITE)
    ChanceText_Rect = ChanceText.get_rect()
    ChanceText_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT - 50)
    DISPLAYSURF.blit(ChanceText, ChanceText_Rect)

def FoundText(found, total):
    # Transparent Overlay---------------------------------------------------------
    for alpha in range(25):
        Overlay = pygame.Surface((SCR_WIDTH, SCR_HEIGHT))  # the size of your rect
        Overlay.set_alpha(alpha)                # alpha level
        Overlay.fill(WHITE)           # this fills the entire surface
        DISPLAYSURF.blit(Overlay, (0,0))    # (0,0) are the top-left coordinates
        pygame.display.update()
    #-----------------------------------------------------------------------------
    FONT_SIZE = 60 # Font size for 'FoundText'
    FontObj = pygame.font.Font('SHOWG.ttf', FONT_SIZE)
    Text = FontObj.render('FOUND '+str(found)+'/'+str(total), True, BLUE)
    Text_Rect = Text.get_rect()
    Text_Rect.center = (SCR_WIDTH/2, SCR_HEIGHT/2+20)
    DISPLAYSURF.blit(Text, Text_Rect)
    pygame.display.update()
    pygame.time.wait(800)

def GameWon(board): # check if Game(is)Won. (it goes through each box in OUR_BOXES...
    #...and checks if it is present in SEL_BOX_LIST, if all of them are in SEL_BOX_LIST...
    #...then GameWon, otherwise carry on.)
    for box in OUR_BOXES:
        left, top = LeftTopOf(board, BoxRowColTup = box)
        BoxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        if BoxRect not in SEL_BOX_LIST:
            return False
    return True

def ReturnItsData(Name): # To get data of 'Name'.
    rec = ''
    RecFile = open('Record.txt', 'r') # open our (Record)'s file..
    RecData = RecFile.readlines() #..read each line of it and store it in RecData..
    RecFile.close()
    Rec = []
    for each in RecData: #..iterate through RecData and append 'each' of it in Rec..
        Rec.append(each.split('::')) 
    for data in Rec: #..next iterate through Rec and..
        #..check if that (data)'s first element is Name..
        if data[0] == Name:
            rec = 'NAME: '+data[0]+'\n'+data[1] #..if yes! then store its info. in 'rec'..
            break
    return rec #..finally return 'rec'.

def BlinkWinningBoards(): # To show the winning boxes for a fraction of time.
    pygame.time.wait(500)
    for each in OUR_BOXES: 
        row, col = each
        left = (col * (BOXSIZE + GAPSIZE) - (BOXSIZE + GAPSIZE)) + XMARGIN
        top = (row * (BOXSIZE + GAPSIZE) - (BOXSIZE + GAPSIZE)) + YMARGIN
        DrawHoverBox(left, top, board)
    pygame.time.wait(100) # here is the time to wait after drawing the boxes.
#----------------------------------------------------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GAMER's CLASS ~~~~~~~~~~~~~~~
now = time.localtime()
class Gamer :
    PLAY = 0
    scrDict = {}
    def __init__(self, name):
        self.Name = name
    def AddScore(self, scr): # add score to scrDict.
        Gamer.PLAY +=1
        KEY = 'GAME '+str(Gamer.PLAY)
        Gamer.scrDict[KEY] = scr
    def AddToRecords(self): # add scrDict to Records file.
        Gamer.PLAY = 0
        RecFile = open('Record.txt', 'a')
        RecFile.write(self.Name + '::' + str(Gamer.scrDict)+'\n')
        RecFile.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# to read Records file before staring the game -------
RecFile = open('Record.txt', 'r')
RecData = RecFile.readlines()
Rec = []
for each in RecData:
    Rec.append(each.split('::'))    
RecFile.close()
#-----------------------------------------------------

Ch = ['1', '2', '3'] # all of our choices the user can give input.

print 'Hey there! do you wish to : '
print '     1. Play as new player.'
print '     2. View a previous record, or'
print '     3. Quit the game.'

Choice = raw_input('You may enter your choice (number of corresponding choice) here: ') # getting Choice.
while Choice not in Ch: # to ensure the Choice is in our decided choice(list Ch above)
    print 'Please enter an appropriate choice,'
    Choice = raw_input('here: ')
    os.system('cls')
    print '     1. Play as new player.'
    print '     2. View a previous record, or'
    print '     3. Quit the game.'

while Choice <> Ch[2]: # run the game as long as Choice is not '3'(which is EXIT from game).
    # reading Records file and storing its info. in Rec.
    RecFile = open('Record.txt', 'r')
    RecData = RecFile.readlines()
    Rec = []
    for each in RecData:
        Rec.append(each.split('::'))    
    RecFile.close()
    
    if Choice == Ch[0]: # now if Choice is '1'(or PLAY the game).
        os.system('cls') # clear commandline's screen.
        NAME = raw_input("So, What should I name you? (or type 'B' or 'b' to go back to menu) ") # getting name of user.
        NAMES = [] # extracting NAMES from Rec.
        for data in Rec:
            NAMES.append(data[0])
        while NAME in NAMES or len(NAME) == 0: # now check if user is trying to play as Name which is already in Records.
            os.system('cls')
            if NAME in NAMES:
                print 'It seems like there is already a record named ', '"',NAME,'"'
                print 'Please try another name to keep your record.'
                NAME = raw_input("(or type 'B' or 'b' to go back to menu): ")
            elif len(NAME) == 0:
                NAME = raw_input("Please enter an appropriate name (or type 'B' or 'b' to go back to menu): ")                    
                    
        if NAME in ['B','b']: # if user enters 'b' or 'B' as NAME then take him to main menu.
            Choice = 'nothing'
        else: # other wise start the game.....
            pygame.init()
            #-------------- DISPLAY -----------------------------------------
            Display = pygame.display.Info()
            SCR_HEIGHT = Display.current_h
            SCR_WIDTH = Display.current_w
            DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.FULLSCREEN)
            pygame.display.set_caption('Buscar')
            #----------------------------------------------------------------
                    
            START = True
            board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
            while START:
                SCORE = 0
                gamer = Gamer(NAME)
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
                        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): # if ESC was pressed.
                            gamer.AddScore(SCORE) # add user's score to his class(Gamer).
                            del SEL_BOX_LIST [:] # Empty SEL_BOX_LIST and OUR_BOXES list when game is over..
                            del OUR_BOXES[:]
                            BOARD_WIDTH = 4 # return BOARD's WIDTH and HEIGHT back to 4...
                            BOARD_HEIGHT = 4
                            #...X and Y MARGIN back to its original value...
                            XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                            YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                            BGCOLOR = (30, 30, 30) #...BGOLOR to its original value.
                            #...and reset level and total boxes to find.
                            level = 1
                            total = level + 2
                            gamer.AddToRecords() # add score to Records file.
                            RecFile = open('Record.txt', 'r') # read Records file again.
                            RecData = RecFile.readlines()
                            START_BUTTON_ON = True
                            START = False
                        elif event.type == KEYUP and event.key == K_RETURN: # If Enter was pressed.
                            START_BUTTON_ON = True # Now Start Button is 'ON'
                        elif event.type == MOUSEMOTION:
                            mousex, mousey = event.pos
                        elif event.type == MOUSEBUTTONUP: # If button was clicked..
                            mousex, mousey = event.pos
                            if StartButton_Rect.collidepoint(mousex, mousey): #..check if StartButton..
                                #...was clicked
                                START_BUTTON_ON = True # Now Start Button is 'ON'
                                
                #---------------------------- INITIALS -----------------
                if not START: # check if START is 'False'...
                    START_BUTTON_ON = False
                    pygame.quit()
                    GO = 'GAME OVER'
                    os.system('cls')
                    for each in GO:
                        print each,
                        time.sleep(0.1)
                else: #...otherwise proceed with the game.
                    board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
                    found = 0
                    level = 1
                    total = level+2
                    OurBoxes = RandomBoxes(board, level)
                    chance = 1
                    BGCOLOR = (30, 30, 30)
                    BOX_COLOR =(255, 0, 0)
                    DISPLAYSURF.fill(BGCOLOR)
                    DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                    FoundText(found, total)
                    DISPLAYSURF.fill(BGCOLOR)
                    DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                    pygame.display.update()
                    BlinkWinningBoards() # blink winning boards.
                #------------------------------------------------------------------------
                    
                while START_BUTTON_ON: # Finally Start Button is clicked (or, it is 'ON').
                    #--- Drawing - board (again, but without Animation), ReturnToHome and PrintChance -----
                    DISPLAYSURF.fill(BGCOLOR)
                    ReturnToHome(True)
                    PrintChance(chance)
                    board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
                    DrawBoard(board, SEL_BOX_LIST)
                    #--------------------------------------------------------------------------------------
                    
                    # redefining X and Y MARGINs, just because BOARDs WIDTH is changed after each level.
                    XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                    YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                    ReturnToHome_Rect = ReturnToHome()
                    mouseClicked = False # Initially mouse isn't Clicked.
                    
                    for event in pygame.event.get(): # event handling loop
                        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): # if ESC was pressed.
                            gamer.AddScore(SCORE) # add user's score.
                            del SEL_BOX_LIST [:] # Empty SEL_BOX_LIST and OUR_BOXES list when game is over..
                            del OUR_BOXES[:]
                            BOARD_WIDTH = 4 # return BOARD's WIDTH and HEIGHT back to 4...
                            BOARD_HEIGHT = 4
                            #...X and Y MARGIN back to its original value...
                            XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                            YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                            BGCOLOR = (30, 30, 30) #...BGOLOR to its original value...
                            level = 1 #...and level and total boxes to default value.
                            total = level + 2
                            START_BUTTON_ON = False
                            gamer.AddToRecords() # addd score to Records to file
                            RecFile = open('Record.txt', 'r') # update our information about Records file.
                            RecData = RecFile.readlines()
                            START = False
                        elif event.type == MOUSEMOTION:
                            mousex, mousey = event.pos
                        elif event.type == MOUSEBUTTONDOWN:# here we check if left or right mouse button (only) was pressed.
                            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                                mousex, mousey = event.pos
                                mouseClicked = True
                    
                    if MouseHoverSomeBox(mousex, mousey, board): # if mouse hovers over some box.
                        DrawHoverBox(mousex, mousey, board) # draw hover box over it.   
                    if mouseClicked:
                        RecFile = open('Record.txt', 'r')
                        RecData = RecFile.readlines()
                        if ReturnToHome_Rect.collidepoint(mousex, mousey): # if user clicks on ReturnToHome button.
                            gamer.AddScore(SCORE)
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
                            SCORE += 10
                            if GameWon(board): #...otherwise proceed here.
                                GameWonAnimation()#...Display GameWonAnimation.
                                level+=1
                                total = level+2
                                # to generate the random color for Background and Boxes ---------
                                RR = randint(0,100)
                                RG = randint(0,100)
                                RB = randint(0,100)
                                BGCOLOR = (RR, RG, RB)
                                RR = randint(100,255)
                                RG = randint(100,255)
                                RB = randint(100,255)
                                BOX_COLOR = (RR, RG, RB)
                                #----------------------------------------------------------------
                                # here  we increase the length or breadth of board as per some conditions --------------
                                if BOARD_WIDTH <= 6 or BOARD_HEIGHT > 8:
                                    BOARD_WIDTH  += 2 # Increase the BOARD's WIDTH.
                                    if BOARD_WIDTH >= 26 : # When board is full.
                                        gamer.AddScore(SCORE)
                                        START_BUTTON_ON = False
                                        START = False
                                        gamer.AddToRecords()
                                        RecFile = open('Record.txt', 'r')
                                        RecData = RecFile.readlines()
                                    else:                                        
                                        #--------------------------- And the same process ------------
                                        XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                                        YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                                        OurBoxes = RandomBoxes(board, level)
                                        #-------------------------------------------------------------
                                elif BOARD_WIDTH >6 and  BOARD_HEIGHT <=8:
                                    BOARD_HEIGHT  += 2 # Increase the BOARD's WIDTH.
                                    if BOARD_WIDTH >= 26 : # When board is full.
                                        gamer.AddScore(SCORE)
                                        START_BUTTON_ON = False
                                        START = False
                                        gamer.AddToRecords()
                                        RecFile = open('Record.txt', 'r')
                                        RecData = RecFile.readlines()
                                    else:
                                        #--------------------------- And the same process ------------
                                        XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                                        YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                                        OurBoxes = RandomBoxes(board, level)
                                        #-------------------------------------------------------------
                                #---------------------------------------------------------------------------------------

                                found = 0
                                if BOARD_WIDTH < 26: # when board is not full..
                                    pygame.time.wait(2000)
                                    board = CreateBoard(BOARD_HEIGHT, BOARD_WIDTH) # Here is our board.
                                    DISPLAYSURF.fill(BGCOLOR)
                                    DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                                    FoundText(found, total) # show FoundText
                                    DISPLAYSURF.fill(BGCOLOR)
                                    DrawBoard(board, SEL_BOX_LIST) # Draw Board.
                                    pygame.display.update()
                                    BlinkWinningBoards() # draw Winning Boards.
                        elif MouseCollideSomeBox(mousex, mousey, board):# If mouse was...
                            #...clicked on any box...
                            SCORE -= 5
                            if chance == 5: #...and if chance is equal to 5 (Finally..)...
                                GameOverAnimation() #...display GameOverAnimation. 
                                BOARD_WIDTH = 4 # return BOARD's WIDTH and HEIGHT back to 4...
                                BOARD_HEIGHT = 4
                                #...X and Y MARGIN back to its original value...
                                XMARGIN = int((SCR_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
                                YMARGIN = int((SCR_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)
                                BGCOLOR = (30, 30, 30) #...BGOLOR to its original value...
                                #...and reset level and total ships to find.
                                level = 1
                                total = level + 2
                                pygame.time.wait(2000)
                                START_BUTTON_ON = False
                                gamer.AddScore(SCORE)
                                break
                            chance+=1 # Increase the chances.
                    pygame.display.update()
                    
                    if not START: # when START is False.
                        pygame.quit() # quit pygame
                        if BOARD_WIDTH >= 26: # and if board was full...
                            os.system('cls')
                            print 'CONGRATULATIONS!'
                            print 'You have completed the game'
                            time.sleep(5)
                        else: #...otherwise proceed here.
                            os.system('cls')
                            GO = 'GAME OVER'
                            for each in GO:
                                print each,
                                time.sleep(0.1)
            os.system('cls')
    
    elif Choice == Ch[1]: # if Choice is give '2'(or display user's history).
        os.system('cls')
        print 'Enter the name you wish to know the record of,'
        Ask = raw_input('here: ') # getting the name of user.
        RecFile = open('Record.txt', 'r')
        RecData = RecFile.readlines()
        Rec = []
        for each in RecData:
            Rec.append(each.split('::'))    
        RecFile.close()
        for data in Rec:
            if Ask == data[0]: # finding data in Records file.
                os.system('cls')
                print ReturnItsData(Ask)
                Enter = raw_input('Press Enter to continue to main menu...')
                break
        else: # if user's name was not found in Records file.
            os.system('cls')
            print 'Sorry! No record for','"',Ask,'"'
            time.sleep(1)
            back = 'Going back to menu....'
            for each in back:
                print each,
                time.sleep(0.1)

    os.system('cls')               
    print 'Hey there! do you wish to : '
    print '     1. Play as new player.'
    print '     2. View a previous record, or'
    print '     3. Quit the game.'
    Choice = raw_input('You may enter your choice (number of corresponding choice) here: ')
    while Choice not in Ch:
        os.system('cls')
        print '     1. Play as new player.'
        print '     2. View a previous record, or'
        print '     3. Quit the game.'
        print 'Please enter an appropriate choice,'
        Choice = raw_input('here: ')
    os.system('cls')
    
#--------------- closing the game ---------------
os.system('cls')
BYE = 'Good Bye user...'
for each in BYE:
    print each,
    time.sleep(0.1)
time.sleep(0.25)
