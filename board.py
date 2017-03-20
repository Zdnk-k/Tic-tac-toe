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
        self.win_condition = 3 if size <= 5 else 4

    def print_board(self):
        """prints playboard"""
        for i in range(self.size):
            for j in range(self.size):
                print(self.array[i][j], end=' ')
            print()
        print()

    def place_symbol(self, coords, symbol):
        """places player symbol on given coordinates the board"""
        x, y = coords
        self.array[y - 1][x - 1] = symbol

    def out_of_bounds(self, x, y):
        """Check if coords out of game plan"""
        return x < 0 or y < 0 or x >= self.size or y >= self.size

    def free_pos(self, x, y):
        """check if cell is free"""
        return self.array[y][x] == '_ '

    def check_win(self, player):
        """check if round was won"""
        for i in range(self.size):
            for j in range(self.size):
                if self.check_row(j, i, player.symbol) \
                    or self.check_column(j, i, player.symbol) \
                    or self.check_diagonaly(j, i, player.symbol):
                    return True
        return False

    def check_row(self, x, y, player_symbol):
        """checks rows from left to rigth"""
        if x + self.win_condition > self.size:
            return False
        for i in range(self.win_condition):
            if self.array[y][x + i] != player_symbol:
                # about to win check for AI
                return False
        return True

    def check_column(self, x, y, player_symbol):
        """checks columns from top to bottom"""
        if y + self.win_condition > self.size:
            return False
        for i in range(self.win_condition):
            if self.array[y + i][x] != player_symbol:
                return False
        return True

    def check_diagonaly(self, x, y, player_symbol):
        """checks both diagonals"""
        result = False
        if (x - self.win_condition) + 1 >= 0 and y + self.win_condition <= self.size:
            result = self.diagonal_tr_bl(x, y, player_symbol)
        if not result:  # if not on first diagonal check second
            if x + self.win_condition <= self.size and y + self.win_condition <= self.size:
                result = self.diagonal_tl_br(x, y, player_symbol)
        return result

    def diagonal_tl_br(self, x, y, player_symbol):
        """checks diagonaly top left -> bottom rigth"""
        for k in range(self.win_condition):
            if self.array[y + k][x + k] != player_symbol:
                return False
        return True

    def diagonal_tr_bl(self, x, y, player_symbol):
        """checks diagonaly top right -> bottom left"""
        for k in range(self.win_condition):
            if self.array[y + k][x - k] != player_symbol:
                return False
        return True

    def reset(self):
        self.array = [['_ '] * self.size for i in range(self.size)]

