#
# Final Project: Final Deliverables
#
# Name: Ryan Nguyen
#

import random
import time

class Board:
    """A data type representing a traditional Battleship
       board with ten rows and ten columns.
    """

    def __init__(self):
        """Construct objects of type Board, with a width of 10 and height of 10"""
        self.data = [['-']*10 for row in range(10)]



    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        game = ''
        rowCount = 0
        colCount = 65

        for row in range(11):
            if row == 0:
                game += '  |'
            elif row > 0 and row < 10:
                game += ' ' + str(rowCount) + '|'
            else:
                game += str(rowCount) + '|'

            for col in range(10):
                if row == 0:
                    game += chr(colCount) + ' '
                else:
                    game += self.data[row-1][col] + ' '

                colCount += 1
            game += '\n'
            rowCount += 1
        return game
    


    def addShipAllowed(self, row, col, length, orient):
        """Arguments:
              row: a number representing the row where the ship wants to be added
                 according to the numbers aligned on the Board (i.e., 1 corresponds
                 to the first row and not 0, and the last row is 10 not 9)
              col: a string representing the column where the ship wants to be added
                 (i.e., the first row is A and the last row is J)
              length: a number representing the length of the ship
              orient: a string representing whether the ship is horizontal or vertical
           Return value:
              True if the ship can be added and False otherwise
        """
        D = self.data
        colNum = ord(col) - 65
        rowNum = row - 1

        if rowNum < 0 or colNum < 0 or rowNum >= len(D) or colNum  >= len(D[0]):
            return False                            # return False when the ship wants to be added off the board

        if orient == 'horizontal':
            if (colNum+length) > len(D):
                return False                        # return False when any part of the ship is off the board
            for c in range(colNum, colNum+length):
                if D[rowNum][c] != '-':
                    return False                    # return False when any part of the ship is blocked by another
        
        if orient == 'vertical':
            if (rowNum+length) > len(D[0]):
                return False
            for r in range(rowNum, rowNum+length):
                if D[r][colNum] != '-':
                    return False
        
        return True
    


    def addShip(self, row, col, length, orient):
        """Arguments:
              row: a number representing the row where the ship wants to be added
                 according to the numbers aligned on the Board (i.e., 1 corresponds
                 to the first row and not 0, and the last row is 10 not 9)
              col: a string representing the column where the ship wants to be added
                 (i.e., the first row is A and the last row is J)
              length: a number representing the length of the ship
              orient: a string representing whether the ship is horizontal or vertical
           Return value:
              adds a ship onto the board
        """
        D = self.data
        colNum = ord(col) - 65
        rowNum = row - 1

        if self.addShipAllowed(row, col, length, orient):
            if orient == 'horizontal':
                for c in range(colNum, colNum+length):
                    D[rowNum][c] = 'O'
            elif orient == 'vertical':
                for r in range(rowNum, rowNum+length):
                    D[r][colNum] = 'O'



    def addAllShipsAI(self):
        """Random placement of adding the 5 types of ships for a traditional game
        """
        lengths = [5, 4, 3, 3, 2]   # lengths of the different types of ships available to a player
        hOrV = ['horizontal', 'vertical']
        for i in range(len(lengths)):
            row = random.choice(range(10))
            col = chr(random.choice(range(65, 75)))
            length = random.choice(lengths)
            orient = random.choice(hOrV)
            while not self.addShipAllowed(row, col, length, orient):
                row = random.choice(range(10))
                col = chr(random.choice(range(65, 75)))
                length = random.choice(lengths)
                orient = random.choice(hOrV)
            lengths.remove(length)
            self.addShip(row, col, length, orient)



    def clear(self):
        """clears the board that calls it
        """
        D = self.data
        for row in range(len(D)):
            for col in range(len(D[0])):
                self.data[row][col] = '-'
    


    def foundShip(self, length):
        """determines if a ship of a specified length has been found (will be useful for deleting a ship)
        """
        D = self.data

        for row in range(len(D)):
            count = 0
            while count < len(D[0]):
                hitLength = 0
                while count < len(D[0]) and D[row][count].equals('O'):
                    hitLength += 1
                    count += 1
                if hitLength == length:
                    return True
                count += 1
        
        for col in range(len(D[0])):
            count = 0
            while count < len(D):
                hitLength = 0
                while count < len(D) and D[count][col].equals("O"):
                    hitLength += 1
                    count += 1
                if hitLength == length:
                    return True
                count += 1

        return False
    


    def shoot(self, row, col):
        """Arguments:
              row: a number representing the row where the ship wants to be added
                 according to the numbers aligned on the Board (i.e., 1 corresponds
                 to the first row and not 0, and the last row is 10 not 9)
              col: a string representing the column where the ship wants to be added
                 (i.e., the first row is A and the last row is J)
           Return value:
              changes the value of the board to match whether you missed or hit a ship
        """
        D = self.data
        col = col.upper()
        colNum = ord(col) - 65
        rowNum = row - 1

        if rowNum < 0 or colNum < 0 or rowNum >= len(D) or colNum  >= len(D[0]):
            pass
        if D[rowNum][colNum] == '-':
            D[rowNum][colNum] = 'M'
        if D[rowNum][colNum] == 'O':
            D[rowNum][colNum] = 'X'

    

    def shootAIRandom(self):
        """takes a random shot at the board
        """
        row = random.choice(range(10))
        col = chr(random.choice(range(65, 75)))
        self.shoot(row, col)

    

    def shootAI(self):
        """strategic shooting for AI
        """
        D = self.data
        shotTakenStatus = False

        for row in range(len(D)):
            for col in range(len(D[0])):
                if D[row][col] == 'X':
                    if col > 1 and D[row][col-1] != 'M' and D[row][col-1] != 'X':
                        self.shoot(row+1, chr(col+64))
                        shotTakenStatus = True
                        break
                    elif row > 1 and D[row-1][col] != 'M' and D[row-1][col] != 'X':
                        self.shoot(row, chr(col+65))
                        shotTakenStatus = True
                        break
                    elif col < 9 and D[row][col+1] != 'M' and D[row][col+1] != 'X':
                        self.shoot(row+1, chr(col+66))
                        shotTakenStatus = True
                        break
                    elif row < 9 and D[row+1][col] != 'M' and D[row+1][col] != 'X':
                        self.shoot(row+2, chr(col+65))
                        shotTakenStatus = True
                        break
                    else:
                        continue
            if shotTakenStatus:
                break

        if not shotTakenStatus:
            row = random.choice(range(10))
            col = chr(random.choice(range(65, 75)))
            c = ord(col) - 65
            while D[row][c] == 'M' or D[row][c] == 'X':
                row = random.choice(range(10))
                col = chr(random.choice(range(65, 75)))
                c = ord(col) - 65
            self.shoot(row, col)



    def copyShots(self, d2):
        """deep copy of a board but only where shots have been taken
        """
        D = self.data
        D2 = d2.data

        for row in range(len(D2)):
            for col in range(len(D2[0])):
                D2[row][col] = D[row][col]
                if D[row][col] == 'O':
                    D2[row][col] = '-'



    def gameOver(self):
        """Returns True when there are no more unsunk ships and returns False otherwise
        """
        D = self.data
        status = False

        for row in range(len(D)):
            for col in range(len(D[0])):
                if D[row][col] != 'O':
                    status = True
                else:
                    return False
        return status
    


    def setUp(self):
        """the set-up part of Battleship when hosting a game where the player adds ships onto their board
        """
        print("Welcome to Battleship!")
        print("In your arsenal, you have the 5 traditional ships to place onto your board:")
        print("(1) Aircraft Carrier (5 spaces)\n(2) Battleship (4 spaces)\n(3) Submarine (3 spaces)\n(4) Destroyer (3 spaces)\n(5) Patrol Boat (2 spaces)\n")

        numShips = 5
        shipInv = [[1, 'Aircraft Carrier (5 spaces)'], [2, 'Battleship (4 spaces)'], [3,'Submarine (3 spaces)'], [4, 'Destroyer (3 spaces)'], [5, 'Patrol Boat (2 spaces)']]
        while numShips > 0:
            s = "You currently have " + str(numShips) + " ship(s).\n"
            for i in range(len(shipInv)):
                s += '(' + str(shipInv[i][0]) + ') ' + shipInv[i][1] + '\n'
            print(s)
            print(self)
            choice = int(input("Please pick which ship to place."))

            if (choice == 1) and ([1, 'Aircraft Carrier (5 spaces)'] in shipInv):
                col = str(input("Which column (A-J) would you like to place your ship?"))
                row = int(input("Which row (1-10) would you like to place your ship?"))
                hOrV = str(input("Is this ship horizontal or vertical (H/V)?"))
                if hOrV == 'H':
                    orient = "horizontal"
                elif hOrV == 'V':
                    orient = "vertical"
                
                if self.addShipAllowed(row, col, 5, orient):
                    self.addShip(row, col, 5, orient)
                else:
                    while not self.addShipAllowed(row, col, 5, orient):
                        print("I'm sorry, but your ship is either off the board or is blocked by a ship you have already placed.\nPlease try again.")
                        col = str(input("Which column (A-J) would you like to place your ship?"))
                        row = int(input("Which row (1-10) would you like to place your ship?"))
                        hOrV = str(input("Is this ship horizontal or vertical?"))
                        if hOrV == 'H':
                            orient = "horizontal"
                        elif hOrV == 'V':
                            orient = "vertical"

                        if self.addShipAllowed(row, col, 5, orient):
                            self.addShip(row, col, 5, orient)
                numShips -= 1
                shipInv.remove([1, 'Aircraft Carrier (5 spaces)'])
                print("\nThis is your current board:")
                print(self)
                continue
                

            elif choice == 2 and ([2, 'Battleship (4 spaces)'] in shipInv):
                col = str(input("Which column (A-J) would you like to place your ship?"))
                row = int(input("Which row (1-10) would you like to place your ship?"))
                hOrV = str(input("Is this ship horizontal or vertical (H/V)?"))
                if hOrV == 'H':
                    orient = "horizontal"
                elif hOrV == 'V':
                    orient = "vertical"
                
                if self.addShipAllowed(row, col, 4, orient):
                    self.addShip(row, col, 4, orient)
                else:
                    while not self.addShipAllowed(row, col, 4, orient):
                        print("I'm sorry, but your ship is either off the board or is blocked by a ship you have already placed.\nPlease try again.")
                        col = str(input("Which column (A-J) would you like to place your ship?"))
                        row = int(input("Which row (1-10) would you like to place your ship?"))
                        hOrV = str(input("Is this ship horizontal or vertical?"))
                        if hOrV == 'H':
                            orient = "horizontal"
                        elif hOrV == 'V':
                            orient = "vertical"

                        if self.addShipAllowed(row, col, 4, orient):
                            self.addShip(row, col, 4, orient)
                numShips -= 1
                shipInv.remove([2, 'Battleship (4 spaces)'])
                print("\nThis is your current board:")
                print(self)
                continue


            elif choice == 3 and ([3, 'Submarine (3 spaces)'] in shipInv):
                col = str(input("Which column (A-J) would you like to place your ship?"))
                row = int(input("Which row (1-10) would you like to place your ship?"))
                hOrV = str(input("Is this ship horizontal or vertical (H/V)?"))
                if hOrV == 'H':
                    orient = "horizontal"
                elif hOrV == 'V':
                    orient = "vertical"
                
                if self.addShipAllowed(row, col, 3, orient):
                    self.addShip(row, col, 3, orient)
                else:
                    while not self.addShipAllowed(row, col, 3, orient):
                        print("I'm sorry, but your ship is either off the board or is blocked by a ship you have already placed.\nPlease try again.")
                        col = str(input("Which column (A-J) would you like to place your ship?"))
                        row = int(input("Which row (1-10) would you like to place your ship?"))
                        hOrV = str(input("Is this ship horizontal or vertical?"))
                        if hOrV == 'H':
                            orient = "horizontal"
                        elif hOrV == 'V':
                            orient = "vertical"

                        if self.addShipAllowed(row, col, 3, orient):
                            self.addShip(row, col, 3, orient)
                numShips -= 1
                shipInv.remove([3, 'Submarine (3 spaces)'])
                print("\nThis is your current board:")
                print(self)
                continue


            elif choice == 4 and ([4, 'Destroyer (3 spaces)'] in shipInv):
                col = str(input("Which column (A-J) would you like to place your ship?"))
                row = int(input("Which row (1-10) would you like to place your ship?"))
                hOrV = str(input("Is this ship horizontal or vertical (H/V)?"))
                if hOrV == 'H':
                    orient = "horizontal"
                elif hOrV == 'V':
                    orient = "vertical"
                
                if self.addShipAllowed(row, col, 3, orient):
                    self.addShip(row, col, 3, orient)
                else:
                    while not self.addShipAllowed(row, col, 3, orient):
                        print("I'm sorry, but your ship is either off the board or is blocked by a ship you have already placed.\nPlease try again.")
                        col = str(input("Which column (A-J) would you like to place your ship?"))
                        row = int(input("Which row (1-10) would you like to place your ship?"))
                        hOrV = str(input("Is this ship horizontal or vertical?"))
                        if hOrV == 'H':
                            orient = "horizontal"
                        elif hOrV == 'V':
                            orient = "vertical"

                        if self.addShipAllowed(row, col, 3, orient):
                            self.addShip(row, col, 3, orient)
                numShips -= 1
                shipInv.remove([4, 'Destroyer (3 spaces)'])
                print("\nThis is your current board:")
                print(self)
                continue


            elif choice == 5 and ([5, 'Patrol Boat (2 spaces)'] in shipInv):
                col = str(input("Which column (A-J) would you like to place your ship?"))
                row = int(input("Which row (1-10) would you like to place your ship?"))
                hOrV = str(input("Is this ship horizontal or vertical (H/V)?"))
                if hOrV == 'H':
                    orient = "horizontal"
                elif hOrV == 'V':
                    orient = "vertical"
                
                if self.addShipAllowed(row, col, 2, orient):
                    self.addShip(row, col, 2, orient)
                else:
                    while not self.addShipAllowed(row, col, 2, orient):
                        print("I'm sorry, but your ship is either off the board or is blocked by a ship you have already placed.\nPlease try again.")
                        col = str(input("Which column (A-J) would you like to place your ship?"))
                        row = int(input("Which row (1-10) would you like to place your ship?"))
                        hOrV = str(input("Is this ship horizontal or vertical?"))
                        if hOrV == 'H':
                            orient = "horizontal"
                        elif hOrV == 'V':
                            orient = "vertical"

                        if self.addShipAllowed(row, col, 2, orient):
                            self.addShip(row, col, 2, orient)
                numShips -= 1
                shipInv.remove([5, 'Patrol Boat (2 spaces)'])
                print("\nThis is your current board:")
                print(self)
                continue

            else:
                print("Bad choice (To be later improved)")
                continue
    


def hostGameAIRandom():
    """plays a game of Battleship with an AI making random moves
    """
    player = Board()
    comp = Board()
    playerSee = Board() # what the player sees
    compSee = Board() # what the computer sees

    comp.addAllShipsAI()
    player.setUp()
    # player.addAllShipsAI() # for testing

    print("Now that you've finished setting up the board, it's time to shoot!\n")
    print(playerSee)

    while not player.gameOver() and not comp.gameOver():
        print("Here are the shots that you have taken currently:")
        print(playerSee)
        # print(comp) # for testing
        choiceShootCol = str(input("Which column would you like to shoot?"))
        choiceShootRow = int(input("Which row would you like to shoot?"))
        # Okay, this looks weird future Ryan, but the computer board is being shot at, not the computer is shooting. Careful distinction to make, my friend...
        comp.shoot(choiceShootRow, choiceShootCol)
        comp.copyShots(playerSee)
        print("\nShot fired!")
        print(playerSee)
        if comp.gameOver(): # need a check here or the game will let the computer make a move even though the player won
            break
        time.sleep(2)
        print("Let's see where the computer shot!")
        player.shootAIRandom()
        player.copyShots(compSee) # This is for later use when developing the smart AI
        print(player)
        time.sleep(2)

    if player.gameOver():
        print("You lose. I guess computers really will take over the world...")
    elif comp.gameOver():
        print("Excellent work! You win! Death to computers!!! Humans #1 forevahhh!!")



def hostGamePvP():
    """plays a game of Battleship with 2 players
    """
    player1 = Board()
    player2 = Board()
    player1See = Board() # what the player1 sees
    player2See = Board() # what the player2 sees

    ready1 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to set up your board, Player 1'))  # 15 lines works for me to not see the last player's board, but ymmv
    if ready1.upper() == 'Y':
        player1.setup()
    
    ready2 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to set up your board, Player 2'))  # 15 lines works for me to not see the last player's board, but ymmv
    if ready2.upper() == 'Y':
        player2.setup()

    # player1.addAllShipsAI() # For testing
    # player2.addAllShipsAI()

    print("Now that you've finished setting up the board, it's time to play!")

    while not player1.gameOver() and not player2.gameOver():
        ready1 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to continue for Player 1'))
        if ready1.upper() == 'Y':
            print("This is your board, Player 1:")
            print(player1)
            print("Here is your opponent's board, Player 1:")
            print(player1See)
            choice1ShootCol = str(input("Which column would you like to shoot?"))
            choice1ShootRow = int(input("Which row would you like to shoot?"))
            player2.shoot(choice1ShootRow, choice1ShootCol)
            player2.copyShots(player1See)
            print("\nShot fired.")
            print(player1See)
            if player2.gameOver(): # need a check here or the game will let Player 2 make a move even though the player won
                break
            time.sleep(2)

        ready2 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to continue for Player 2'))
        if ready2.upper() == 'Y':
            print("This is your board, Player 2:")
            print(player2)
            print("Here is your opponent's board, Player 2:")
            print(player2See)
            choice2ShootCol = str(input("Which column would you like to shoot?"))
            choice2ShootRow = int(input("Which row would you like to shoot?"))
            player1.shoot(choice2ShootRow, choice2ShootCol)
            player1.copyShots(player2See)
            print("\nShot fired.")
            print(player2See)
            time.sleep(2)

    if player1.gameOver():
        print("PLAYER 2 WINS!!!!")
    elif player2.gameOver():
        print("PLAYER 1 WINS!!!!")



def hostGameAI():
    """plays a game of Battleship with a non-random, smart AI
    """
    player = Board()
    comp = Board()
    playerSee = Board() # what the player sees

    comp.addAllShipsAI()
    player.setUp()
    # player.addAllShipsAI() # for testing

    print("Now that you've finished setting up the board, it's time to shoot!\n")
    print(playerSee)

    while not player.gameOver() and not comp.gameOver():
        print("Here are the shots that you have taken currently:")
        print(playerSee)
        # print(comp) # for testing
        choiceShootCol = str(input("Which column would you like to shoot?"))
        choiceShootRow = int(input("Which row would you like to shoot?"))
        comp.shoot(choiceShootRow, choiceShootCol)
        comp.copyShots(playerSee)
        print("\nShot fired!")
        print(playerSee)
        # print(comp) # for testing
        if comp.gameOver(): # need a check here or the game will let the computer make a move even though the player won
            break
        time.sleep(2)
        print("Let's see where the computer shot!")
        player.shootAI()
        print(player)
        time.sleep(2)

    if player.gameOver():
        print("You lose. I guess computers really will take over the world...")
    elif comp.gameOver():
        print("Excellent work! You win! Death to computers!!! Humans #1 forevahhh!!")



def hostGameGraderAI():
    """plays a game with the non-random AI but allows you to see where the ships are of the computer's board and sets up your ship
       WARNING!! You will think that you're so much smarter than the AI, but once you play blind--run hostGameAI()--you may nearly lose like I did T-T
    """
    player = Board()
    comp = Board()
    playerSee = Board() # what the player sees

    comp.addAllShipsAI()
    player.addAllShipsAI() # for testing

    print("Now that you've finished setting up the board, it's time to shoot!\n")
    print(playerSee)

    while not player.gameOver() and not comp.gameOver():
        print("Here are the shots that you have taken currently:")
        print(comp) # for testing
        choiceShootCol = str(input("Which column would you like to shoot?"))
        choiceShootRow = int(input("Which row would you like to shoot?"))
        comp.shoot(choiceShootRow, choiceShootCol)
        comp.copyShots(playerSee)
        print("\nShot fired!")
        print(comp)
        if comp.gameOver(): # need a check here or the game will let the computer make a move even though the player won
            break
        time.sleep(2)
        print("Let's see where the computer shot!")
        player.shootAI()
        print(player)
        time.sleep(2)

    if player.gameOver():
        print("You lose. I guess computers really will take over the world...")
    elif comp.gameOver():
        print("Excellent work! You win! Death to computers!!! Humans #1 forevahhh!!")



def hostGameGraderPvP():
    """plays a game of Battleship with 2 players but allows you to see the opponent's board and sets up your ships for you
    """
    player1 = Board()
    player2 = Board()

    player1.addAllShipsAI()
    player2.addAllShipsAI()

    print("Now that you've finished setting up the board, it's time to play!")

    while not player1.gameOver() and not player2.gameOver():
        ready1 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to continue for Player 1'))
        if ready1.upper() == 'Y':
            print("This is your board, Player 1:")
            print(player1)
            print("Here is your opponent's board, Player 1:")
            print(player2)
            choice1ShootCol = str(input("Which column would you like to shoot?"))
            choice1ShootRow = int(input("Which row would you like to shoot?"))
            player2.shoot(choice1ShootRow, choice1ShootCol)
            print("\nShot fired.")
            print(player2)
            if player2.gameOver(): # need a check here or the game will let Player 2 make a move even though the player won
                break
            time.sleep(2)

        ready2 = str(input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nType "Y" to continue for Player 2'))
        if ready2.upper() == 'Y':
            print("This is your board, Player 2:")
            print(player2)
            print("Here is your opponent's board, Player 2:")
            print(player1)
            choice2ShootCol = str(input("Which column would you like to shoot?"))
            choice2ShootRow = int(input("Which row would you like to shoot?"))
            player1.shoot(choice2ShootRow, choice2ShootCol)
            print("\nShot fired.")
            print(player1)
            time.sleep(2)

    if player1.gameOver():
        print("PLAYER 2 WINS!!!!")
    elif player2.gameOver():
        print("PLAYER 1 WINS!!!!")