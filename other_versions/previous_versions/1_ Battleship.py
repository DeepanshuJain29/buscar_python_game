from random import randint
import time

board = []

for x in range(5):
    board.append(["O"] * 5)

def print_board(board):
    for row in board:
        print " ".join(row)

print "Let's play Battleship!"
print_board(board)

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

#Main game loop
for turn in range(3): #Loop executes 3 times to give 3 chances to the users
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



