import networkx as nx


class Game:
    def __init__(self):
        self.node = None  # initializing current node
        self.first_move = True  # if it's the first move starting node doesn't matter
        self.player_turn = 'A'  # it's player A's turn
        self.g = nx.DiGraph()
        self.g.add_weighted_edges_from([(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (2, 4, 1)])  # initializing graph

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

    def maximizer(self):
        max_value = -2  # initializes max value to less than possible minimum
        move_start = None
        move_end = None

        if self.evaluate() == 'A':
            return 1, 0, 0
        elif self.evaluate() == "B":
            return -1, 0, 0

        for move in self.legal_moves():
            self.node = move[1]
            self.g[move[0]][move[1]]['weight'] -= 1
            if self.first_move:
                self.first_move = False
                was_first_move = True
            else:
                was_first_move = False

            if self.minimizer()[0] > max_value:
                print(max_value)
                max_value = self.minimizer()[0]
                move_start = move[0]
                move_end = move[1]
                print(self.minimizer()[0])
                print(self.minimizer())

            if was_first_move:
                self.first_move = True
                self.node = None
            if not was_first_move:
                self.node = move[0]
            self.g[move[0]][move[1]]['weight'] += 1

        return max_value, move_start, move_end

    def minimizer(self):
        min_value = 2
        move_start = None
        move_end = None

        if self.evaluate() == 'A':
            return 1, 0, 0
        elif self.evaluate() == "B":
            return -1, 0, 0

        for move in self.legal_moves():
            self.node = move[1]
            self.g[move[0]][move[1]]['weight'] -= 1

            if self.maximizer()[0] < min_value:
                min_value = self.maximizer()[0]
                move_start = move[0]
                move_end = move[1]

            self.node = move[0]
            self.g[move[0]][move[1]]['weight'] += 1

            return min_value, move_start, move_end

    def solve(self):
        while True:
            print(self.maximizer())
            print(self.node)
            best_move = self.maximizer()
            self.g[best_move[1]][best_move[2]]['weight'] -= 1
            self.node = best_move[2]
            print(self.node)
            if self.first_move:
                self.first_move = False
            if not self.legal_moves():
                return self.player_turn
            if self.player_turn == 'A':
                self.player_turn = 'B'
            else:
                self.player_turn = 'A'


print(Game().maximizer())
