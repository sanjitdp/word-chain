import networkx as nx
import time


class Game:
    def __init__(self):
        self.node = None  # initializing current node
        self.first_move = True  # if it's the first move starting node doesn't matter
        self.player_turn = 'A'  # it's player A's turn
        self.g = nx.DiGraph()
        self.g.add_weighted_edges_from([(1, 2, 7), (2, 1, 6), (2, 3, 1), (3, 4, 1), (4, 1, 1), (2, 4, 1)])
        # initializing graph

    def legal_moves(self):
        legal = []
        if self.first_move:  # if it's your first move, all possible moves are legal
            for edge in self.g.edges(data=True):
                if edge[2]['weight'] > 0:
                    legal.append([edge[0], edge[1]])
        else:  # if it's not your first move, check if the move starts at the current node
            for edge in self.g.edges(data=True):
                if edge[2]['weight'] > 0 and edge[0] == self.node:
                    legal.append([edge[0], edge[1]])
        return legal

    def game_ended(self):
        if self.first_move and self.g.out_degree == 0:  # there are no outgoing edges on the graph at all
            return True
        elif not self.first_move and self.g.out_degree(self.node, weight='weight') == 0:
            # there are no outgoing edges from your current node
            return True
        else:
            return False

    def evaluate(self):  # determine whether somebody has won the game, and if so, who
        if self.game_ended() and self.player_turn == 'A':
            return 'A'
        elif self.game_ended() and self.player_turn == 'B':
            return 'B'
        else:
            return None

    def switch_turn(self):
        if self.player_turn == 'A':
            self.player_turn = 'B'
        else:
            self.player_turn = 'A'

    def maximizer(self, alpha, beta):
        max_value = -2  # initializes max value to less than possible minimum
        move_start = None
        move_end = None

        winner = self.evaluate()
        if winner == 'A':  # check whether the game has ended and return
            return 1, 0, 0
        elif winner == 'B':
            return -1, 0, 0

        for move in self.legal_moves():
            self.node = move[1]  # set the current node to be the second node listed in the edge
            self.g[move[0]][move[1]]['weight'] -= 1  # remove one from the weight of the node (word was used up)
            if self.first_move:
                # end first move but remember to treat it as the first move when we come back to this board position
                self.first_move = False
                was_first_move = True
            else:
                was_first_move = False
            self.switch_turn()

            next_min_value = self.minimizer(alpha, beta)
            if next_min_value[0] > max_value:
                # set the maximum value to the minimum value of the next move
                max_value = next_min_value[0]
                move_start = move[0]
                move_end = move[1]

            if was_first_move:  # pop and reset the board to its prior position
                self.first_move = True
                self.node = None
            else:
                self.node = move[0]
            self.g[move[0]][move[1]]['weight'] += 1
            self.switch_turn()

            if max_value >= beta:
                return max_value, move_start, move_end
            if max_value > alpha:
                alpha = max_value

        return max_value, move_start, move_end
        # return the maximum value (1 if win and -1 if lose) and end the turn

    def minimizer(self, alpha, beta):  # minimizes expected score every alternate turn, similar to maximizer
        min_value = 2
        move_start = None
        move_end = None

        winner = self.evaluate()
        if winner == 'A':
            return 1, 0, 0
        elif winner == 'B':
            return -1, 0, 0

        for move in self.legal_moves():
            self.node = move[1]
            self.g[move[0]][move[1]]['weight'] -= 1

            next_max_value = self.maximizer(alpha, beta)
            if next_max_value[0] < min_value:
                min_value = next_max_value[0]
                move_start = move[0]
                move_end = move[1]

            self.node = move[0]
            self.g[move[0]][move[1]]['weight'] += 1
            if self.player_turn == 'A':
                self.player_turn = 'B'
            else:
                self.player_turn = 'B'

            if min_value <= alpha:
                return min_value, move_start, move_end
            if min_value < beta:
                beta = min_value

        return min_value, move_start, move_end

    def solve(self):  # maximizes/minimizes every alternate turn and returns the winner
        i = 0
        while True:
            best_move = self.maximizer(-2, 2)
            if self.game_ended() and best_move[0] == 1:
                return 'A wins the game.'
            elif self.game_ended() and best_move[0] == -1:
                return 'B wins the game.'

            if i % 2 == 0:
                print('A:', best_move[1:])
            else:
                print('B:', best_move[1:])
            i += 1

            self.g[best_move[1]][best_move[2]]['weight'] -= 1
            self.node = best_move[2]
            if self.first_move:
                self.first_move = False


start_time = time.time()
print(Game().solve(), '\n')
end_time = time.time()
print('Evaluation time: {}s'.format(end_time-start_time))
