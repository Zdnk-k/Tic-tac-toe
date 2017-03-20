import board
import player
import sys

"""
================================================================================
------------------------------- GAME CLASS -------------------------------------
================================================================================
"""
class Game(object):
    def __init__(self, p1, p2, board):
        self.player1 = p1   # player 1
        self.player2 = p2   # player 2
        self.board = board # playboard
        self.current_player = self.player1

    """
    ------------- GAME SHIT --------------------
    """
    def player_turn(self):
        """execute player turn"""
        print("\nPlayer: {}    Score: {}".format(self.current_player.name, self.current_player.score))  # prints game info, whose turn and score
        self.board.print_board()    # print board_sizes
        coords = self.get_coords()  # get coords from player
        self.board.place_symbol(coords, self.current_player.symbol)    # place player symbol on board

    def play_round(self):
        """plays one round"""
        self.set_first_player() # set starting player
        round_end = False       # end cause won or no empty slots == draw
        round_won = False       # round won by player
        cant_play = False       # no empty positions
        turn = 1                # counts turns
        while not round_end:
            self.player_turn()  # selects starting player
            if turn >= self.board.win_condition:    # only checks after some turns played
                round_won = self.board.check_win(self.current_player)
                cant_play = turn == self.board.size ** 2 # if of turns == of cells
                round_end =  round_won or cant_play # ends if round is won/no empty positions
            if not round_end: # if round not finnished
                turn += 1   # iterate turns
                self.change_players()    # change active player

        if round_won:   # if round won by one of the players
            print("\n{} is a proper cunt!\n".format(self.current_player.name))
            self.current_player.add_score()    # adds score to winner
            self.set_next_first_player()    # next round starting player
        else:  # if not won, it's a draw
            print("\nIT'S A DRAW!")
        self.board.print_board()    # print bord whe ngame endds


    def correct_player_turn(self, coords):
        """Checks if given coordinates are correct"""
        x, y = coords
        if coords == None:
            return False
        elif len(coords) != 2:
            print("x and y, that's exactly 2 coordinates, can't be that hard to understand....")
            return False
        elif self.board.out_of_bounds(x - 1, y - 1):    # if coords out of bounds
            print('Position out of bounds!')
            return False
        elif not self.board.free_pos(x - 1, y - 1):  # if coords already taken
            print('Position already taken!')
            return False
        return True

    def get_coords(self):
        """Get coords of the cell from player"""
        while True:
            try:
                coords = tuple(map(int, input('y, x = ').split(',')))
                while not self.correct_player_turn(coords):
                    coords = tuple(map(int, input('y, x = ').split(',')))   # coordinates as a tuple
                return coords
            except ValueError:
                print("Oppsy daisy! That's not a corect input! 'x,y'")

    def send_coords(self, coords):
        pass

    def set_first_player(self):
        """sets the first player based on od previous round winner"""
        if self.player2.won_previous:
            self.current_player = self.player2
        else: self.current_player = self.player1

    def set_next_first_player(self):
        """sets winners won_previous parameter ot true so he will star the next round"""
        if self.current_player == self.player1:
            self.player1.won_previous = True
            self.player2.won_previous = False
        else:
            self.player2.won_previous = True
            self.player1.won_previous = False

    def change_players(self):
        """changes players"""
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_again(self):
        """ask if player wants another round"""
        play_again = input("Do you wish to play again??? (yes/no): ")
        while True:
            if play_again in ('Yes', 'yes', 'y', 'YES', 'yep', 'yarp', 'aye'):
                return True
            elif play_again in ('No', 'no', 'n', 'nope', 'NO', 'nay'):
                return False
            else:
                print('God dammit Sir, can you no write??')
            play_again = input("Play again??? (It's simple, just type yes/no): ")

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
        print('Farewell!')
        sys.exit()

    def uber_check_win(self):
        """ checks the total winner(rounds won) """
        if self.player1.score == self.player2.score:
            print("It's a draw!")
        elif self.player1.score > self.player2.score:
            print("Player 1 is a proper bad ass mother fucker")
        else:
            print("Player numma 2 is a proper bad ass mother fucker")

