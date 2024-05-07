from random import randint
import traceback

class bot():
    def __init__(self) -> None:
        pass

    def select_move(self, possible_moves):
        pass

class human_player(bot):
    def select_move(self, possible_moves):
        selected = False
        while not selected:
            move = self.get_move()
            try:
                move = int(move)
            except:
                print("Input has to be an integer!")
                continue
            if(move > len(possible_moves) or move < 1):
                print(f"Input has to be an integer between 1 and {len(possible_moves)}!")
                continue
            selected = True
        return possible_moves[move-1]
    
    def get_move(self):
        return input(f'Select move: ')

class random_bot(bot):
    def select_move(self, possible_moves):
        try:
            if(len(possible_moves)-1 == 0):
                return possible_moves[0]
            return possible_moves[randint(0, len(possible_moves)-1)]
        except Exception as error:
            print(traceback.format_exc())
            print(possible_moves)
    
class exp_min_max(bot):
    def select_move(self, possible_moves):
        pass

class mcts_bot(bot):
    def __init__(self, game) -> None:
        args = {
            'C': 1.41, # sqrt of 2
            'num_searches': 100 #Budget per rollout
        }
        mcts = MCTS(game, args)
        super().__init__()

    def select_move(self, possible_moves):
        pass
    
            
