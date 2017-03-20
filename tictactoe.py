import player as p
import game as g
import board as b


class GameSettings(object):
    def __init__(self):
        self.game = None
        self.p1 = None
        self.p2 = None
        self.board = None
    
    def start_game(self):
        pass
    
    def set_game(self):
        pass
    
    def game_settings(self):
        pass

if __name__ == "__main__":
    p1 = p.HumanPlayer("Player1", 'X')
    p2 = p.HumanPlayer("Player2", 'O')
    board = b.Board(3)
    game = g.Game(p1, p2, board)
    game.play()