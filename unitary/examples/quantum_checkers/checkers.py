from enums import CheckersResult, CheckersRules, Colors
from typing import List
from copy import deepcopy

# GLOBAL GAME SETTINGS
forced_take = True


class Move:
    def __init__(self, start_row, start_col, end_row, end_col) -> None:
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col


class Checkers:
    def __init__(self, num_rows=5, num_cols=5, num_rows_pieces=1) -> None:
        self.board = Board(num_rows, num_cols, num_rows_pieces)
        pass

    def result(self):
        """
        returns:
            UNFINISHED = 0
            White wins = 1
            Black wins = 2
            DRAW = 3
            BOTH_WIN = 4
        """
        if (
            len(self.board.calculate_all_possible_moves(Colors.WHITE)) == 0
            and len(self.board.calculate_all_possible_moves(Colors.BLACK)) == 0
        ):
            return CheckersResult.DRAW
        elif len(self.board.calculate_all_possible_moves(Colors.WHITE)) == 0:
            return CheckersResult.WHITE_WINS
        elif len(self.board.calculate_all_possible_moves(Colors.BLACK)) == 0:
            return CheckersResult.BLACK_WINS
        else:
            return CheckersResult.UNFINISHED

    def do_move(self, move: Move):
        self.board.move_piece(
            move.start_row, move.start_col, move.end_row, move.end_col
        )
        print(move.start_row, move.start_col, move.end_row, move.end_col)


class Square:
    def __init__(self) -> None:
        self.occupant = None


class Board:
    def __init__(self, num_rows, num_cols, num_rows_pieces) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Initalize empty board
        # test = Square()
        self.board_matrix = [
            [Square() for x in range(self.num_cols)] for x in range(self.num_rows)
        ]
        if num_rows_pieces * 2 >= num_rows:
            print(
                f"Too many rows ({num_rows_pieces}) filled with pieces. Decrease this number for this size of board. [{num_rows}]x[{num_cols}]"
            )
            exit()

        # Initialize pieces on correct squares
        for y in range(num_rows_pieces):
            for x in range(self.num_cols):
                if y % 2 == 0 and x % 2 == 0:
                    self.board_matrix[y][x].occupant = Piece(Colors.BLACK)
                    self.board_matrix[self.num_rows - 1 - y][x].occupant = Piece(
                        Colors.WHITE
                    )

                elif y % 2 != 0 and x % 2 != 0:
                    self.board_matrix[y][x].occupant = Piece(Colors.BLACK)
                    self.board_matrix[self.num_rows - 1 - y][x].occupant = Piece(
                        Colors.WHITE
                    )

        # self.board_matrix[1][3].occupant = Piece(Colors.WHITE)
        # Test to see if king works
        # self.board_matrix[4][4].occupant = Piece(Colors.BLACK, king=True)
        # self.board_matrix[4][5].occupant = Piece(Colors.WHITE)
        # self.board_matrix[3][3].occupant = Piece(Colors.WHITE)
        # self.board_matrix[3][5].occupant = Piece(Colors.WHITE)

    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Moves a piece from given row and column to given row and column. Changes it into a king if it reaches the end
        """
        # self.board_matrix[to_row][to_col].occupant = deepcopy(self.board_matrix[from_row][from_col].occupant)
        self.board_matrix[to_row][to_col].occupant = Piece(
            self.board_matrix[from_row][from_col].occupant.color,
            self.board_matrix[from_row][from_col].occupant.king,
        )
        self.remove_piece(from_row, from_col)

        # If jumping over a piece, we need to remove it aswell
        # Jump from column 2 over 3 to 4 we add 3+(3-2)
        # Jump from column 3 over 2 to 1 we add 2+(2-3)
        # jump_row = i.end_row+(i.end_row-i.start_row)
        if abs(to_row - from_row) > 1:
            self.remove_piece(
                int((to_row + from_row) / 2), int((to_col + from_col) / 2)
            )

        # If it is not a king and reaches the end it needs to be kinged
        if self.board_matrix[to_row][to_col].occupant.king == False and (
            to_row == 0 or to_row == self.num_rows - 1
        ):
            self.board_matrix[to_row][to_col].occupant.king = True
        return

    def remove_piece(self, row, col):
        self.board_matrix[row][col].occupant = None
        return

    def print_board(self):
        output = "\n"
        output += "   |"
        for i in range(self.num_cols):
            output += f" {i} |"
        output += "\n" + "---|" * (self.num_cols + 1)
        output += "\n"
        for i in range(self.num_rows):
            output += f" {i} |"
            for j in range(self.num_cols):
                # print(f"{self.board_matrix[i][j].occupant.color}")
                if self.board_matrix[i][j].occupant != None:
                    # print(self.board_matrix[i][j].occupant.color)
                    if self.board_matrix[i][j].occupant.color == Colors.WHITE:
                        if self.board_matrix[i][j].occupant.king == True:
                            output += " W "
                        else:
                            output += " w "
                    else:
                        if self.board_matrix[i][j].occupant.king:
                            output += " B "
                        else:
                            output += " b "
                    # print(type(self.board_matrix[i][j].occupant))
                    # output += f" {self.board_matrix[i][j].occupant.color} "
                else:
                    output += "   "
                output += "|"
            output += "\n" + "---|" * (self.num_cols + 1)
            output += "\n"
        return output

    def calculate_all_possible_moves(self, color: Colors):
        legal_moves = []
        legal_take_moves = []
        # Loop over all squares, if there is a piece there check what moves are possible.
        # Moves will be
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (
                    self.board_matrix[i][j].occupant != None
                    and self.board_matrix[i][j].occupant.color == color
                ):
                    # temp1, temp2 = self.calculate_legal_move(i, j, color)
                    # legal_moves.extend(temp1)
                    # legal_take_moves.extend(temp2)
                    temp_legal_moves, temp_take_moves = self.possible_moves(i, j)
                    legal_moves.extend(temp_legal_moves)
                    legal_take_moves.extend(temp_take_moves)
        if len(legal_take_moves) != 0 and forced_take:
            return legal_take_moves
        return legal_moves

    def on_board(self, row, col):
        """
        Checks if given location is on the board on not.
        Returns true if [row][col] is on the board
        """
        if row < 0 or row > self.num_rows - 1 or col < 0 or col > self.num_cols - 1:
            return False
        return True

    def possible_blind_moves(self, row, col):
        """
        Returns for one piece the possible moves that pieces can move in without checking if that moves is on the board or if there is a piece in the way
        Returns empty list if there is no piece
        """
        legal_moves = []
        if self.board_matrix[row][col].occupant != None:
            if self.board_matrix[row][col].occupant.king == False:
                if (
                    self.board_matrix[row][col].occupant.color == Colors.WHITE
                ):  # White non king piece
                    legal_moves.append(Move(row, col, row - 1, col - 1))
                    legal_moves.append(Move(row, col, row - 1, col + 1))
                else:  # Black non king piece
                    legal_moves.append(Move(row, col, row + 1, col - 1))
                    legal_moves.append(Move(row, col, row + 1, col + 1))
            else:  # King piece can move in all directions
                legal_moves.append(Move(row, col, row - 1, col - 1))
                legal_moves.append(Move(row, col, row - 1, col + 1))
                legal_moves.append(Move(row, col, row + 1, col - 1))
                legal_moves.append(Move(row, col, row + 1, col + 1))
        return legal_moves

    def possible_moves(self, row, col):  # For one
        """
        For one piece, calculate all legal moves
        """
        legal_moves = self.possible_blind_moves(row, col)
        new_legal_moves = []  # all possible moves
        take_moves = []  # Moves that take another piece
        for i in legal_moves:
            # For each move, check if the coordinates are on the board
            # If so, check if it is empty. If so, it is a legal move
            # If there is another piece, check if it is a different color than your own color
            # If so, check if one square further is empty
            # If so you can take a piece
            if self.on_board(i.end_row, i.end_col):  # Coordinate is on board
                if self.board_matrix[i.end_row][i.end_col].occupant == None:  # Empty
                    # print(f"{i.end_row},{i.end_col}")
                    new_legal_moves.append(i)
                elif (
                    self.board_matrix[i.end_row][i.end_col].occupant.color
                    != self.board_matrix[i.start_row][i.start_col].occupant.color
                ):
                    # Different color so we have to check if we can jump over
                    # Jump from column 2 over 3 to 4 we add 3+(3-2)
                    # Jump from column 3 over 2 to 1 we add 2+(2-3)
                    jump_row = i.end_row + (i.end_row - i.start_row)
                    jump_col = i.end_col + (i.end_col - i.start_col)
                    if (
                        self.on_board(jump_row, jump_col)
                        and self.board_matrix[jump_row][jump_col].occupant == None
                    ):  # we can jump over. For readibility not in previous if statement
                        new_legal_moves.append(
                            Move(i.start_row, i.start_col, jump_row, jump_col)
                        )
                        take_moves.append(
                            Move(i.start_row, i.start_col, jump_row, jump_col)
                        )
        return new_legal_moves, take_moves


class Piece:
    def __init__(self, color=None, king=False) -> None:
        self.color = color
        self.king = king


class GameInterface:
    def __init__(self, game: Checkers) -> None:
        self.game = game
        self.player = Colors.WHITE

    def get_move(self):
        return input(f"Player {self.player.name} to move: ")

    def play(self):
        while self.game.result() == CheckersResult.UNFINISHED:
            self.print_board()
            legal_moves = self.print_legal_moves()
            move = self.get_move()
            try:
                move = int(move)
            except:
                print("Input has to be an integer!")
                continue
            if move > len(legal_moves) or move < 1:
                print(f"Input has to be an integer between 1 and {len(legal_moves)}!")
                continue
            self.game.do_move(legal_moves[move - 1])

            self.player = Colors.BLACK if self.player == Colors.WHITE else Colors.WHITE

    def print_board(self):
        print(self.game.board.print_board())

    def get_legal_moves(self):
        """
        Returns list of legal moves
        """
        return self.game.board.calculate_all_possible_moves(self.player)

    def print_legal_moves(self):
        """
        Prints all legal moves and returns list of legal moves
        """
        index = 1
        print(f"Legal moves for player {self.player.name}:")
        legal_moves = self.game.board.calculate_all_possible_moves(self.player)
        for i in legal_moves:
            print(
                f"{index}. [{i.start_col}][{i.start_row}] to [{i.end_col}][{i.end_row}]"
            )
            index += 1
        return legal_moves


def main():
    game = GameInterface(Checkers())
    # game.print_board()
    # game.print_legal_moves()
    game.play()


if __name__ == "__main__":
    main()
