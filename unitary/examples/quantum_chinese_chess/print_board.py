
def print_board():
    num_rows = 10
    board_string = "";
    board_string += " ";
    for col in 'abcdefghi':
      board_string += " %c"%col
    board_string += "\n";
    for row in range(num_rows):
      board_string += "%d "%row;
      for col in 'abcdefghi':
#          board_string += "车"
#          board_string += ". "
          board_string += "R "
#          board_string += PieceAt(col, row).symbol()
#        Piece p = pieceAt(col, row);
#        if p == null:
#          board_string += " .";
#        else:
#          switch (p.rank) {
#            case ROOK: board_string += p.isRed ? " R" : " r"; break;
#            case KNIGHT: board_string += p.isRed ? " N" : " n"; break;
#            case BISHOP: board_string += p.isRed ? " B" : " b"; break;
#            case GUARD: board_string += p.isRed ? " G" : " g"; break;
#            case KING: board_string += p.isRed ? " K" : " k"; break;
#            case CANNON: board_string += p.isRed ? " C" : " c"; break;
#            case PAWN: board_string += p.isRed ? " P" : " p"; break;
#          }
      board_string += " %d\n"%row
    board_string += " "
    for col in 'abcdefghi':
      board_string += " %c"%col
    print(board_string)

print_board()

from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
