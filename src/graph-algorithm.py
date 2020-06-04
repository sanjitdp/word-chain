import networkx as nx


class Game:
    def __init__(self):
        self.node = 1
        self.first_move = True
        self.player_turn = 'a'
        self.g = nx.DiGraph()
        self.g.add_weighted_edges_from([(1, 2, 0), (2, 3, 1), (3, 1, 0), (1, 1, 0)])

    def legal_moves(self):
        legal = []
        if self.first_move:
            for (u, v, d) in self.g.edges(data=True):
                if d['weight'] > 0:
                    legal.append([u, v])
        else:
            for (u, v, d) in self.g.edges(data=True):
                if d['weight'] > 0 and u == self.node:
                    legal.append([u, v])
        return legal

    def game_ended(self):
        if self.first_move and self.g.out_degree == 0:
            return True
        elif not self.first_move and self.g.out_degree(self.node, weight='weight') == 0:
            return True
        else:
            return False

    def evaluate(self):
        if self.game_ended() and self.player_turn == 'a':
            return 1
        elif self.game_ended() and self.player_turn == 'b':
            return -1
        else:
            return 0

    def maximizer(self):
        max_value = -2
        move_u = None
        move_v = None
        self.evaluate()
        for (u, v) in self.legal_moves():
            self.node = v
            self.g[u][v]['weight'] -= 1
            if self.minimizer()[1] > max_value:
                max_value = self.minimizer()[1]
                move_u = u
                move_v = v
        return [max_value, move_u, move_v]

    def minimizer(self):
        min_value = 2
        move_u = None
        move_v = None
        self.evaluate()
        for (u, v) in self.legal_moves():
            self.node = v
            self.g[u][v]['weight'] -= 1
            if self.minimizer()[1] < min_value:
                min_value = self.maximizer()[1]
                move_u = u
                move_v = v
        return [min_value, move_u, move_v]

    def solve(self):
        while True:
            if self.evaluate != 0:
                if self.evaluate() == 1:
                    print('A has won.')
                elif self.evaluate() == -1:
                    print('B has won.')
                return
            if self.player_turn == 'a':
                (m, u, v) = self.maximizer()
                self.node = v
                self.player_turn = 'b'
            if self.player_turn == 'b':
                (u, v) = self.maximizer()
                self.node = v
                self.player_turn = 'a'


print(Game().solve()) # solve the game
