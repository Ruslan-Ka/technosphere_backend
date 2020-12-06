import os
import time
import sys


class TicTacGame:
    """Class realize Tic-Tac-Toe"""
    count = 0
    token = 'X'
    board = None

    def show_board(self):
        """Print the board."""
        print ("-------------")
        for i in range(3):
            print ("|", self.board[0+i*3], "|", self.board[1+i*3], "|", self.board[2+i*3], "|")
            print ("-------------")

    def validate_input(self, turn):
        """Validate user input."""
        os.system('clear')
        while True:
            try:
                my_turn = int(turn)
            except ValueError:
                os.system('clear')
                print("Your input is incorrect")
                time.sleep(2)
                self.show_board()
                turn = input("Choose a cell for your turn\n")
                continue
            else:
                if my_turn in self.board:
                    self.board[my_turn - 1] = self.token
                    self.check_winner()
                else:
                    os.system('clear')
                    print("There is no empty cell on the board for your input")
                    time.sleep(2)
                    self.show_board()
                    turn = input("Choose a cell for your turn\n")
                    continue

    def new_turn(self):
        """Accept user input."""
        self.count += 1
        self.show_board()
        turn = input("Player {} Choose a cell for your turn\n".format(self.token))
        self.validate_input(turn)

    def start_game(self):
        "Clean the board and start new game."""
        self.count = 0
        self.board = list(range(1,10))
        os.system('clear')
        self.new_turn()

    def wanna_play(self):
        "Ask user about a new game."""
        while True:
            ans = input("Do you want to play again?[Y/N]\n")
            if ans == 'N':
                print("Bye!")
                sys.exit()
            elif ans == 'Y':
                self.start_game()
            else:
                print("Incorrect input")
                continue

    def check_winner(self):
        """Check the board for a winner."""
        win_list = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
        for i in win_list:
            if self.board[i[0]] == self.board[i[1]] == self.board[i[2]]:
                self.show_board()
                print("Won by the {} player!".format(self.token))
                time.sleep(2)
                self.wanna_play()
        if self.token == 'X':
            self.token = 'O'
        else:
            self.token = 'X'
        if self.count == 9:
            self.show_board()
            print("Draw!")
            time.sleep(2)
            self.wanna_play()
        else:
            self.new_turn()


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
