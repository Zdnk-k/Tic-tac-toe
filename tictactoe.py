import sys
import time

"""
================================================================================
------------------------------- GAME CLASS -------------------------------------
================================================================================
"""
class Game(object):
    def __init__(self, p1, p2, board_size):
        self.player1 = p1   # player 1
        self.player2 = p2   # player 2
        self.board = Board(board_size)  # playboard

    """
    ------------- GAME SHIT --------------------
    """
    def player_turn(self, actual_player):
        """execute player turn"""
        print("\nPlayer: {}    Score: {}".format(actual_player.name, actual_player.score))  # prints game info, whose turn and score
        self.board.print_board()    # print board_sizes
        coords = self.get_coords()  # get coords from player
        self.board.place_symbol(coords[1], coords[0], actual_player.symbol)    # place player symbol on board

    def play_round(self):
        """plays one round"""
        actual_player = self.set_first_player()   # set starting player
        round_end = False   # end cause won or no empty slots == draw
        round_won = False   # round won by player
        cant_play = False   # no empty positions
        turn = 1  # counts turns
        while not round_end:
            self.player_turn(actual_player) # selects starting player
            if turn >= self.board.win_condition:    # only checks after some turns played
                round_won = self.board.check_win(actual_player)
                cant_play = turn == self.board.size ** 2 # if no. of turns == no. of positions
                round_end =  round_won or cant_play # ends if round is won/no empty positions
            if not round_end: # if round not finnished
                turn += 1   # iterate turns
                actual_player = self.change_players(actual_player)    # change active player

        if round_won:   # if round won by one of the players
            print("\n{} is a proper cunt!\n".format(actual_player.name))
            actual_player.add_score()    # adds score to winner
            self.set_next_first_player(actual_player)    # next round starting player
        else:  # if not won, it's a draw
            print("\nIT'S A DRAW!")
        self.board.print_board()    # print bord whe ngame endds
        # TODO: draw
        # TODO: reset
        # TODO: second player won

    def correct_player_turn(self, coords):
        """Checks if given coordinates are correct"""
        if coords == None:
            return False
        elif len(coords) != 2:
            print("x and y, that's exactly 2 coordinates, can't be that hard to understand....")
            return False
        elif self.board.out_of_bounds(coords):    # if coords out of bounds
            print('Position out of bounds!')
            return False
        elif self.board.already_taken(coords):  # if coords already taken
            print('Position already taken!')
            return False
        return True

    def get_coords(self):
        """Get coords of the cell from player"""
        while True:
            try:
                coords = None
                while not self.correct_player_turn(coords):
                    coords = list(map(int, input('y, x = ').split(',')))   # coordinates as a tuple
                    coords = [a - 1 for a in coords]    # convert coords
                return coords
            except ValueError:
                print("Oppsy daisy! That's not a corect input!")

    def set_first_player(self):
        """sets the first player based on od previous round winner"""
        if self.player2.won_previous:
            return self.player2
        return self.player1

    def set_next_first_player(self, actual_player):
        """sets winners won_previous parameter ot true so he will star the next round"""
        if actual_player == self.player1:
            self.player1.won_previous = True
            self.player2.won_previous = False
        else:
            self.player2.won_previous = True
            self.player1.won_previous = False

    def change_players(self, actual_player):
        """chenges players"""
        if actual_player == self.player1:
            return self.player2
        else:
            return self.player1

    def play_again(self):
        """ask if player wants another round"""
        play_again = input("Do you wish to play again??? (yes/no)")
        while True:
            if play_again in ('Yes', 'yes', 'y', 'YES', 'yep', 'yarp', 'aye'):
                return True
            elif play_again in ('No', 'no', 'n', 'nope', 'NO', 'nay'):
                return False
            else:
                print('God dammit Sir, can you no write??')
            play_again = input("Play again??? (It's simple, just type yes/no)")

    def play(self):
        """starts a game"""
        quit = False
        wanna_play = True
        while not quit:
            quit = not wanna_play
            while wanna_play:
                self.play_round()
                wanna_play = self.play_again()
                self.board.reset()
        sys.exit()
        time.sleep(3)
        print('Exitting...')

    def uber_check_win(self):
        """ checks the total winner(rounds won) """
        if self.player1.score == self.player2.score:
            print("It's a draw!")
        elif self.player1.score > self.player2.score:
            print("Player 1 is a proper bad ass mother fucker")
        else:
            print("Player numma 2 is a proper bad ass mother fucker")


"""
================================================================================
------------------------------- BOARD CLASS -------------------------------------
================================================================================
"""
class Board(object):
    """represents play board, has methods to print it, place player symbols and check winner"""
    def __init__(self, size):
        self.size = size
        self.array =  [['_ '] * self.size for i in range(self.size)]
        self.win_condition = 3 # TODO: you know...

    def print_board(self):
        """prints playboard"""
        for i in range(self.size):
            for j in range(self.size):
                print(self.array[i][j], end='')
            print()
        print()

    def place_symbol(self, x, y, symbol):
        """places player symbol on given coordinates the board"""
        self.array[y][x] = symbol

    def out_of_bounds(self, coords):
        """Check if coords out of game plan"""
        return coords[0] < 0 or coords[1] < 0 or coords[0] >= self.size or coords[1] >= self.size

    def already_taken(self, coords):
        """check if cell is already taken"""
        pos = self.array[coords[0]][coords[1]]
        return pos == 'O ' or pos == 'X '


    """ ========= check winner ==============="""
    def check_win(self, player):
        """check if round was won"""
        for i in range(self.size):
            for j in range(self.size):
                if self.check_row(j, i, player.symbol) or self.check_column(j, i, player.symbol) or self.check_diagonaly(j, i, player.symbol):
                    return True
        return False

    def check_row(self, x, y, player_symbol):
        """checks rows"""
        if x + self.win_condition > self.size:
            return False
        else:
            for i in range(self.win_condition):
                if self.array[y][x + i] != player_symbol:
                    return False
            return True

    def check_column(self, x, y, player_symbol):
        """checks columns"""
        if y + self.win_condition > self.size:
            return False
        else:
            for i in range(self.win_condition):
                if self.array[y + i][x] != player_symbol:
                    return False
            return True

    def check_diagonaly(self, x, y, player_symbol):
        """checks both diagonals"""
        result = False
        if x + self.win_condition <= self.size and y - self.win_condition + 1 >= 0:
            result = self.diagonal_up(x, y, player_symbol)
        if not result:  # if not on first diagonal check second
            if x + self.win_condition <= self.size and y + self.win_condition <= self.size:
                result = self.diagonal_down(x, y, player_symbol)
        return result

    def diagonal_down(self, x, y, player_symbol):
        """checks top left - right bottom diagonal"""
        for k in range(self.win_condition):
            if self.array[y + k][x + k] != player_symbol:
                return False
        return True

    def diagonal_up(self, x, y, player_symbol):
        """checks left bottom - right top diagonal"""
        for k in range(self.win_condition):
            if self.array[y - k][x + k] != player_symbol:
                return False
        return True

    def reset(self):
        self.array = [['_ '] * self.size for i in range(self.size)]



"""
=========================================================
------------ PLAYER CLASS -------------------------------
=========================================================
"""

class Player(object):
    """
    represents a player
    symbol: players symbol
    """
    def __init__(self, name, symbol, ai):
        self.name = name
        self.symbol = symbol    # players symbol
        self.ai = ai            # if computer controlled player
        self.score = 0          # score = rounds won
        self.won_previous = False    # remember whether he won the previous round (he will start if so)

    def add_score(self):
        """adds points"""
        self.score += 1

    def ai_play(self):
        pass
