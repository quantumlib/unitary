import argparse
from enums import CheckersResult, CheckersRules
from interface import GameInterface
from quantum_checkers import Checkers
import time
from players import * # Imports all possible bots
import os
import glob
import math
import cProfile
import pstats
import os
import glob
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_rows', help='The number of rows of the checkboard. INT', default=8)
    parser.add_argument('--num_columns', help='The number of columns of the checkboard. INT', default=8)
    parser.add_argument('--num_vertical_pieces', help='The number of rows that are filled with checkerpieces. INT', default=1)
    parser.add_argument('--sim_q', help='Simulating quantum or actually use quantum mechanics. TRUE if you want to simulate quantum.', default="False")
    parser.add_argument('--GUI', help='If GUI is enabled. True or False', default="False")
    parser.add_argument('--p1', help='Select agent for player 1 to use.', default=human_player())
    parser.add_argument('--p2', help='Select agent for player 2 to use.', default=human_player())
    args = parser.parse_args()
    p1 = human_player()
    p2 = human_player()
    if(args.num_columns % 2 == 1 and args.num_rows % 2 == 0):
        warning_len = len("# WARNING: If the number of columns is uneven and the number of rows is even the board is not symmetrical. #")
        print("#"*warning_len)
        print("# WARNING: If the number of columns is uneven and the number of rows is even the board is not symmetrical. #\n# To assure an equal number of pieces, set the number of vertical pieces to an even value.                 #")
        print("#"*warning_len)
        time.sleep(5)
    # for rule in [CheckersRules.CLASSICAL, CheckersRules.QUANTUM_V1, CheckersRules.QUANTUM_V2]:
    #     for size in [10, 12, 14]:
    size = 5
    selected = False
    while not selected:
        inp = input(f'Select what rule to use:\n1. Classical\n2. Quantum V1 (superpositions)\n3. Quantum V2 (Simple entanglement)\n4. Quantum V3 (Entanglement)\n')
        try:
            inp = int(inp)
        except:
            print("Input has to be an integer!")
            continue
        if(inp > 4 or inp < 1):
            print(f"Input has to be an integer between 1 and 4!")
            continue
        selected = True
        if(inp == 1): rule = CheckersRules.CLASSICAL
        elif(inp == 2): rule = CheckersRules.QUANTUM_V1
        elif(inp == 3): rule = CheckersRules.QUANTUM_V2
        elif(inp == 4): rule = CheckersRules.QUANTUM_V3
    checkers = Checkers(num_vertical=size, num_horizontal=size, num_vertical_pieces=args.num_vertical_pieces, SIMULATE_QUANTUM=args.sim_q, rules=rule)
    game = GameInterface(checkers, white_player=p1, black_player=p2, GUI=args.GUI)
    _, _ = (game.play())

if __name__ == "__main__":
    main()

# Generate prof:  python3 -m cProfile -o main.prof main.py
# Visualise prof: snakeviz main.prof
