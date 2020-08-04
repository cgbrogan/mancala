import random
from agents import MaxAgent, RandomAgent

class Game():

    def __init__(self):
        
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    
        self.p1_score = self.board[6]
        self.p2_score = self.board[13]

        self.p1_board = self.board[0:6]
        self.p2_board = self.board[7:13]

        self.player_metadata = {1: {'purse_idx': 6,
                                    'legal_actions': [0,1,2,3,4,5]},
                                2: {'purse_idx': 13,
                                    'legal_actions': [7,8,9,10,11,12]}}

        self.active_player = 1
        self.number_of_players = 1

        self.is_over = False

        self.winner = None

    def print_state(self):
        """
        Pretty print the state of the game

          Player 1 Score: xx
          Player 2 Score: xx

          Player Turn: Player x
        
            4 4 4 4 
          0         0
            4 4 4 4
        """
        p1_board = self.board[0:6]
        p2_board = self.board[7:13]
        p2_board.reverse()
        p1_purse = self.board[6]
        p2_purse = self.board[13]

        print('\n')
        print("Player 1 Score: {}".format(self.p1_score))
        print("Player 2 Score: {}".format(self.p2_score))
        print('\n')
        print("Active Player: {}".format(self.active_player))
        print("Actions: ", self.get_legal_actions())
        print("Game Over: {}".format(self.is_over))
        print('\n')
        print('\t   ' + ' '.join(map(str, p2_board)))
        print('\t' + str(p2_purse) + '\t\t' + str(p1_purse))
        print('\t   ' + ' '.join(map(str, p1_board)))
        print('\n')
        print("="*50)
   
    def switch_active_player(self):
        if self.active_player == 1:
            self.active_player = 2
        else:
            self.active_player = 1

    def update_score_and_board(self):
        self.p1_score = self.board[6]
        self.p2_score = self.board[13]
        self.p1_board = self.board[0:6]
        self.p2_board = self.board[7:13]

    def get_legal_actions(self):
        "Return a list of numbers that correspond to the mancala position to move"
        actions = []
        if self.active_player == 1:
            for i in range(0,6):
                if self.board[i] > 0:
                    actions.append(i)
        else:
            for i in range(7,13):
                if self.board[i] > 0:
                    actions.append(i)

        return actions

    def take_action(self, action, is_simulation):
        """Action is an integer repreesenting the spot on the board that the player selected"""
        old_board = self.board.copy()

        legal_actions = self.player_metadata[self.active_player]['legal_actions']
        
        if action not in legal_actions:
            print("ERROR: Illegal board location for Player")
            return None

        stones = self.board[action]
        self.board[action] = 0
        while stones > 0:
            action += 1
            if (self.active_player == 1 and action == 13) or (self.active_player == 2 and action == 6):
                action += 1
            action %= len(self.board)
            self.board[action] += 1
            stones -= 1

        last_action = action
        # Don't go again if the final position is not in your purse
        if last_action != self.player_metadata[self.active_player]['purse_idx']:
            self.switch_active_player()

        # If a player lands on their side, and the opposite side has marbles
        # then the player takes both their side and the opposing side, assuming
        # their side was empty before landing 
        # 0<->7 1<->8, 2<->9, 3<->10, 4<->11, 5<->12
        if last_action in legal_actions:
            stones = self.board[last_action]
            opponent_stones = self.board[(last_action + 7) % len(self.board)]
            opponent_idx = (last_action + 7) % len(self.board)
            if stones == 1:
                if opponent_stones > 0:
                    purse_idx = self.player_metadata[self.active_player]['purse_idx']
                    self.board[purse_idx] += stones + opponent_stones
                    self.board[last_action] = 0
                    self.board[opponent_idx] = 0

        if is_simulation:
            self.board = old_board

        self.update_score_and_board()
        self.is_game_over()

        if self.is_over:
            self.p1_score += sum(self.p1_board)
            self.p2_score += sum(self.p2_board)

    def is_game_over(self):
        p1_is_over = True
        p2_is_over = True
        
        for stones in self.p1_board:
            if stones > 0:
                p1_is_over = False
                break

        for stones in self.p2_board:
            if stones > 0:
                p2_is_over = False
                break

        self.is_over = p1_is_over or p2_is_over
        self.winner = max([self.p1_score, 'P1'], [self.p2_score, 'P2'])[1]


if __name__ == "__main__":
    tally = {}
    # player_1 = RandomAgent()
    # player_2 = MaxAgent()
    for _ in range(1):
        env = Game()
        env.print_state()
        while not env.is_over:
            actions = env.get_legal_actions()
            action = random.choice(actions)
            # if env.active_player == 1:
            #     # RandomAgent
            #     actions = env.get_legal_actions()
            #     action = random.choice(actions)
            # if env.active_player == 2:
            #     # MaxAgent
            #     actions = env.get_legal_actions()
            #     action = random.choice(actions)
            print("Player {} - Action: {}".format(str(env.active_player), str(action)))
            env.take_action(action, False)
            env.print_state()

        # If you want to play multiple games
        if env.winner in tally:
            tally[env.winner] += 1
        else:
            tally[env.winner] = 1

    print("P1 Score: ", env.p1_score)
    print("P2 Score: ", env.p2_score)
    print("Board sum: ", sum(env.board))
    print("Done")

