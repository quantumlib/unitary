from quantum_checkers import Checkers, Move_id
from players import human_player

import numpy as np
import pygame
import random
from time import sleep
from enums import CheckersResult, CheckersPlayer, MoveType
import os
from pygame import gfxdraw
import time

# GUI
import pygame
import sys
from copy import deepcopy

# https://quantumchess.net/play/
# https://entanglement-chess.netlify.app/qm
# https://github.com/quantumlib/unitary/blob/main/docs/unitary/getting_started.ipynb

# GLOBAL GUI SETTINGS
# Constants
WIDTH, HEIGHT = 600, 600
SQUARE_W, SQUARE_H = 60, 60
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (51, 51, 51)
DARK_BROWN = (145, 94, 42)
LIGHT_BROWN = (231, 203, 175)
YELLOW = (230, 225, 7)
L_RED = (221, 0, 0)
RED = (180, 2, 1)
BLUE = (0, 0, 255)
CROWN_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), "crown.png"))
CROWN_IMG = pygame.transform.smoothscale(
    CROWN_IMG,
    (
        int(SQUARE_W * 0.65),
        int((CROWN_IMG.get_height() / (CROWN_IMG.get_width() / SQUARE_W)) * 0.65),
    ),
)
RED_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "images/Damsteen-rood.png")
)
RED_IMG = pygame.transform.smoothscale(
    RED_IMG,
    (int(SQUARE_W), int((RED_IMG.get_height() / (RED_IMG.get_width() / SQUARE_W)))),
)
RED_SELECTED_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "images/Damsteen-rood-geselecteerd.png")
)
RED_SELECTED_IMG = pygame.transform.smoothscale(
    RED_SELECTED_IMG,
    (
        int(SQUARE_W),
        int(
            (RED_SELECTED_IMG.get_height() / (RED_SELECTED_IMG.get_width() / SQUARE_W))
        ),
    ),
)

BLACK_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "images/Damsteen-zwart.png")
)
BLACK_IMG = pygame.transform.smoothscale(
    BLACK_IMG,
    (int(SQUARE_W), int((BLACK_IMG.get_height() / (BLACK_IMG.get_width() / SQUARE_W)))),
)
BLACK_SELECTED_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "images/Damsteen-zwart-geselecteerd.png")
)
BLACK_SELECTED_IMG = pygame.transform.smoothscale(
    BLACK_SELECTED_IMG,
    (
        int(SQUARE_W),
        int(
            (
                BLACK_SELECTED_IMG.get_height()
                / (BLACK_SELECTED_IMG.get_width() / SQUARE_W)
            )
        ),
    ),
)

BLUE_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "images/Damsteen-geest.png")
)
BLUE_IMG = pygame.transform.smoothscale(
    BLUE_IMG,
    (int(SQUARE_W), int((BLUE_IMG.get_height() / (BLUE_IMG.get_width() / SQUARE_W)))),
)


class GameInterface:
    def __init__(self, game: Checkers, white_player, black_player, GUI=False) -> None:
        self.game = game
        self.quit = False
        self.highlighted_squares = []
        self.selected_id = (
            None  # Square select by player, used for highlighting and moving pieces
        )
        self.move_locations = (
            set()
        )  # If a piece is selected, this variable will store the locations the piece can move to
        if GUI.lower() == "true":
            self.GUI = True
            self.init_gui()
        else:
            self.GUI = False
        self.draw_chance = False
        self.white_player = white_player
        self.black_player = black_player
        # self.black_player = MCTS(self.game, self.args)

    def init_gui(self):
        pygame.init()
        # Initialize the screen
        infoObject = pygame.display.Info()
        width = self.game.num_horizontal * SQUARE_W
        height = self.game.num_vertical * SQUARE_H
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Quantum Checkers")
        # Clock to control the frame rate
        clock = pygame.time.Clock()

    def highlight_squares(self, moves_list: list):
        self.highlighted_squares = []
        self.move_locations.clear()
        movable_pieces = []
        for move in moves_list:
            movable_pieces.append(move.source_id)
            if move.source_id == self.selected_id:
                self.move_locations.add(move.target1_id)
        if len(self.move_locations) > 0:
            self.highlighted_squares.append(self.selected_id)
            for i in self.move_locations:
                self.highlighted_squares.append(i)
            return
        # no piece selected that is able to move TODO
        for idx in movable_pieces:
            self.highlighted_squares.append(idx)

    def play(self):
        counter = 0
        moves = []
        prev_take = False  # variable to check if a piece has been taken before
        # for i in [3, 2, 2, 1, 1, 2, 2, 1]:
        #     # legal_moves = self.get_legal_moves()
        #     self.game.player_move(self.game.legal_moves[i-1], self.game.player)
        #     self.print_board(False)
        while self.game.status == CheckersResult.UNFINISHED and not self.quit:
            if self.GUI:
                if self.game.player == CheckersPlayer.WHITE and not isinstance(
                    self.white_player, human_player
                ):
                    move = self.white_player.select_move(self.game.legal_moves)
                    self.do_game_move(move)
                    prev_take = False
                elif self.game.player == CheckersPlayer.BLACK and not isinstance(
                    self.black_player, human_player
                ):
                    # move = self.black_player.search()
                    move = self.white_player.select_move(self.game.legal_moves)
                    self.do_game_move(move)
                # for(i in self.game.related_squares):
                #     if(id in i):
                #     pass

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    if event.type == pygame.MOUSEBUTTONDOWN and (
                        (
                            self.game.player == CheckersPlayer.WHITE
                            and isinstance(self.white_player, human_player)
                        )
                        or (
                            self.game.player == CheckersPlayer.BLACK
                            and isinstance(self.black_player, human_player)
                        )
                    ):
                        down_pos = event.pos
                        # self.handle_click(event.pos)
                    if event.type == pygame.MOUSEBUTTONUP and (
                        (
                            self.game.player == CheckersPlayer.WHITE
                            and isinstance(self.white_player, human_player)
                        )
                        or (
                            self.game.player == CheckersPlayer.BLACK
                            and isinstance(self.black_player, human_player)
                        )
                    ):
                        # Detect swipes for quantum moves
                        moved, _ = self.handle_click(down_pos, event.pos)
                        if moved:
                            self.print_board(False)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.draw_chance = (
                                True if self.draw_chance == False else False
                            )
                    # self.game.player_move(legal_moves[random.randint(1, len(legal_moves))-1], self.game.player)

                    # If it is the humans turn the click event will handle everything
                    # self.print_board()
                    self.highlight_squares(self.game.legal_moves)
                    self.draw_board()
                    pygame.display.flip()  # needs to be called outside draw function
                    # time.sleep(1)
            else:  # ASCII BOARD
                prev_take = False  # Always reset
                attempt_str = ""
                attempt_str = self.game.get_sim_board()
                self.print_board(True)
                self.print_legal_moves(self.game.legal_moves)
                counter += 1
                # if(counter % 10 == 0):
                #     print(f"Move number {counter}")
                # move = random.randint(1, len(legal_moves))
                if self.game.player == CheckersPlayer.WHITE:
                    move = self.white_player.select_move(self.game.legal_moves)
                else:
                    move = self.black_player.select_move(self.game.legal_moves)
                moves.append(move)
                print("Selected move: ", end="")
                move.print_move()
                self.game.player_move(move, self.game.player)
                # if(len(self.game.legal_moves) > 0):
                #     prev_take = True
                # self.write_to_log(move, counter, moves)
                # time.sleep(1)
        # self.print_board()
        print(f"Results: {self.game.status}")
        return (self.game.status, counter)

    def draw_circle(self, id, color, x, y, radius, king=False, highlighted=False):
        if color == RED:
            if highlighted:
                # highlight_color = YELLOW
                c = RED_SELECTED_IMG.get_rect(
                    center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
                )  # centers the image
                self.screen.blit(RED_SELECTED_IMG, c)
            else:
                # highlight_color = RED
                c = RED_IMG.get_rect(
                    center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
                )  # centers the image
                self.screen.blit(RED_IMG, c)
            # gfxdraw.filled_circle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius, highlight_color)
            # gfxdraw.filled_circle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius-int(radius*0.15), L_RED)
            # gfxdraw.aacircle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius-int(radius*0.15), L_RED)
            # gfxdraw.aacircle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius, highlight_color)
        else:
            if highlighted:
                c = BLACK_SELECTED_IMG.get_rect(
                    center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
                )  # centers the image
                self.screen.blit(BLACK_SELECTED_IMG, c)
            else:
                # highlight_color = RED
                c = BLACK_IMG.get_rect(
                    center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
                )  # centers the image
                self.screen.blit(BLACK_IMG, c)
            # gfxdraw.filled_circle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius, highlight_color)
            # gfxdraw.filled_circle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius-int(radius*0.15), GREY)
            # gfxdraw.aacircle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius-int(radius*0.15), GREY)
            # gfxdraw.aacircle(self.screen, x+SQUARE_W//2, y+SQUARE_H//2, radius, highlight_color)
        if king:
            c = CROWN_IMG.get_rect(
                center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
            )  # centers the image
            self.screen.blit(CROWN_IMG, c)
        if self.draw_chance:
            # pygame.font.init() # you have to call this at the start,
            # if you want to use this module.
            my_font = pygame.font.SysFont("Comic Sans MS", 20)
            text_surface = my_font.render(
                str(self.game.classical_squares[str(id)].chance), False, (255, 255, 255)
            )
            text_rect = text_surface.get_rect(
                center=(x + SQUARE_W // 2, y + SQUARE_H // 2)
            )  # centers the image
            self.screen.blit(text_surface, text_rect)

    def get_positions(self, player) -> [[list, list], [list, list]]:
        """
        Gets the positions of all the pieces from the game.
        Returns two lists of lists of the player positions and opponent positions separated by the normal pieces and king pieces
        """
        return self.game.get_positions(player)

    def draw_board(self):
        self.screen.fill(WHITE)
        white_pieces, black_pieces = self.game.get_advanced_positions(
            CheckersPlayer.WHITE
        )
        flip = True
        for id in range(self.game.num_horizontal * self.game.num_vertical):
            # print(f"{id}, {self.game.num_horizontal}, {id % self.game.num_horizontal == 0}")
            if id % self.game.num_horizontal == 0:
                flip = not flip
            x, y = self.game.convert_id_to_xy(id)
            screen_x = x * SQUARE_W
            screen_y = y * SQUARE_H
            if (
                flip and self.game.num_horizontal % 2 == 0
            ):  # For even length we need to flip the board the squares drawn, not for uneven length
                color = DARK_BROWN if (id) % 2 == 0 else LIGHT_BROWN
            else:
                color = LIGHT_BROWN if (id) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(
                self.screen, color, (screen_x, screen_y, SQUARE_W, SQUARE_H)
            )
            highlight = True if (id in self.highlighted_squares) else False
            if str(id) in black_pieces:
                # pygame.draw.circle(self.screen, RED, (screen_x+SQUARE_W//2, screen_y+SQUARE_H//2), int(SQUARE_W-0.15*SQUARE_W)//2)
                self.draw_circle(
                    id,
                    GREY,
                    screen_x,
                    screen_y,
                    int(SQUARE_W - 0.15 * SQUARE_W) // 2,
                    black_pieces[str(id)].king,
                    highlight,
                )
            elif str(id) in white_pieces:
                self.draw_circle(
                    id,
                    RED,
                    screen_x,
                    screen_y,
                    int(SQUARE_W - 0.15 * SQUARE_W) // 2,
                    white_pieces[str(id)].king,
                    highlight,
                )
            elif (
                id in self.highlighted_squares
            ):  # Highlight squares for where the selected piece can move
                gfxdraw.circle(
                    self.screen,
                    screen_x + SQUARE_W // 2,
                    screen_y + SQUARE_H // 2,
                    int(SQUARE_W - 0.15 * SQUARE_W) // 2,
                    WHITE,
                )
                gfxdraw.aacircle(
                    self.screen,
                    screen_x + SQUARE_W // 2,
                    screen_y + SQUARE_H // 2,
                    int(SQUARE_W - 0.15 * SQUARE_W) // 2,
                    WHITE,
                )
                # c = BLUE_IMG.get_rect(center=(screen_x+SQUARE_W//2, screen_y+SQUARE_H//2)) # centers the image
                # self.screen.blit(BLUE_IMG, c)

        # DRAW CONNECTED RELATED PIECES IF THE MOUSE IS HOVERING OVER AN ENTANGLED SQUARE
        x, y = pygame.mouse.get_pos()
        id = self.game.convert_xy_to_id(int(x / SQUARE_W), int(y / SQUARE_H))
        templist = []
        for i in self.game.related_squares:
            if str(id) in i:
                templist = i
                break
        if len(templist) > 0:
            start_x, start_y = self.game.convert_id_to_xy(id)
            start_x = start_x * SQUARE_W + SQUARE_W / 2
            start_y = start_y * SQUARE_H + SQUARE_H / 2
            for i in templist:
                if i == str(id):
                    continue
                end_x, end_y = self.game.convert_id_to_xy(int(i))
                end_x = end_x * SQUARE_W + SQUARE_W / 2
                end_y = end_y * SQUARE_H + SQUARE_H / 2
                pygame.draw.line(
                    self.screen, BLUE, (start_x, start_y), (end_x, end_y), 2
                )

    def get_id_from_mouse_pos(self, x, y):
        x = x // SQUARE_W
        y = y // SQUARE_H
        return self.game.convert_xy_to_id(x, y)

    def do_game_move(self, move: Move_id):
        """
        Do a game move and reset values for GUI
        """
        self.game.player_move(move, self.game.player)
        self.selected_id = (
            -1
        )  # value used in highlight function to check if we need to return
        self.move_locations.clear()
        self.highlighted_squares = []

    def handle_click(self, first_pos, second_pos):
        """
        Handles clicking on the board. Returns true if a move was done
        """
        print("ALL LEGAL MOVES")
        for i in self.game.legal_moves:
            i.print_move()
        self.highlighted_squares = []
        mouse_x, mouse_y = first_pos[0], first_pos[1]
        first_id = self.get_id_from_mouse_pos(mouse_x, mouse_y)
        mouse_x, mouse_y = second_pos[0], second_pos[1]
        second_id = self.get_id_from_mouse_pos(mouse_x, mouse_y)
        if first_id == second_id:
            if (
                self.selected_id is not None
                and self.move_locations is not None
                and first_id in self.move_locations
            ):  # We want to move the piece to first id
                # Find the correct move so the backend handels everything correctly.
                temp_move = None
                for move in self.game.legal_moves:
                    if (
                        move.source_id == self.selected_id
                        and move.target1_id == first_id
                        and move.target2_id == None
                    ):
                        temp_move = move
                        break
                try:
                    temp_move.print_move()
                except:
                    print("Move not found")
                    print(move.source_id, move.target1_id, move.target2_id)
                    print(self.selected_id, first_id, second_id)
                legal_moves = self.do_game_move(temp_move)  # classic move
                return True, legal_moves
            self.selected_id = first_id
            return False, []
        elif (
            self.selected_id is not None
            and self.move_locations is not None
            and first_id in self.move_locations
            and second_id in self.move_locations
        ):
            # Split move
            if int(first_id) > int(second_id):  # Swap them around for the move
                first_id, second_id = second_id, first_id
            temp_move = None
            for move in self.game.legal_moves:
                if (
                    move.source_id == self.selected_id
                    and move.target1_id == first_id
                    and move.target2_id == second_id
                ):
                    temp_move = move
                    break
            try:
                temp_move.print_move()
            except:
                print("Move not found")
                print(move.source_id, move.target1_id, move.target2_id)
                print(self.selected_id, first_id, second_id)
            legal_moves = self.do_game_move(temp_move)  # classic move
            return True, legal_moves
        return False, []

    def print_board(self, simulated: bool) -> str:
        # str_board = self.game.get_sim_board()
        if not simulated:
            str_board = self.game.get_board()
        else:
            str_board = self.game.get_sim_board()
        print(str_board)
        return str_board

    def get_legal_moves(self) -> list:
        moves = self.game.calculate_possible_moves(self.game.player)
        return moves

    def print_legal_moves(self, legal_moves=None) -> list:
        """
        Prints all legal moves the current player can do
        """
        index = 1  # Start counter at 1
        if legal_moves == None:
            legal_moves = self.get_legal_moves()
        for move in legal_moves:
            move.print_move(index=index)
            index += 1
        # print(legal_moves)
        # for key, value in legal_moves.items():
        #     if(type(value) == list and len(value) > 1):
        #         print(f"{str(index)}: [{key}] to [{value[0]}]")
        #         legal_moves_list.append(Move_id(source_id=key, target1_id=value[0]))
        #         index += 1
        #         print(f"{str(index)}: [{key}] to [{value[1]}]")
        #         legal_moves_list.append(Move_id(source_id=key, target1_id=value[1]))
        #         index+=1
        #         print(f"{str(index)}: [{key}] to [{value[0]}] and [{value[1]}]")
        #         legal_moves_list.append(Move_id(source_id=key, target1_id=value[0], target2_id=value[1]))
        #     else:
        #         print(f"{str(index)}: [{key}] to [{value[0]}]")
        #         legal_moves_list.append(Move_id(source_id=key, target1_id=value[0]))
        #     index +=1
        return legal_moves
