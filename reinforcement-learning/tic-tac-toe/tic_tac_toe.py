#! /usr/bin/env python

"""
Functions for experimenting with reinforcement learning in tic-tac-toe.

:author: Robert David Grant <robert.david.grant@gmail.com>

:copyright: Copyright 2011 Robert Grant

    Licensed under the Apache License, Version 2.0 (the "License"); you
    may not use this file except in compliance with the License.  You
    may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.  See the License for the specific language governing
    permissions and limitations under the License.
"""

import random
import itertools
from functools import partial
from os import path
import numpy as np
import numpy.matlib as nm
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt


###############################################################################
# Simulation components
###############################################################################

BLANK = 0
X = 1
O = 2


class Board():
    """Tic-tac-toe board.  0 = blank, 1 = 'x', 2 = 'o'"""
    rep = {BLANK: ' ', 
           X: 'x', 
           O: 'o'}

    def __init__(self):
        """Initialize board to matrix of BLANKs"""
        self.state = nm.ones([3,3], dtype='int32') * BLANK
    
    def __repr__(self):
        return nm.matrix.__repr__(self.state)

    def __str__(self):
        return "\n".join(
                map(lambda row: "|".join((Board.rep[elt] for elt in row)),
                    self.state.tolist()))

    def play(self, side, position):
        """
        Place player's mark on the board, either X or O, at position defined by
        a tuple, e.g. (0,1).
        """
        self.state[position[0], position[1]] = side


def are_winning_rows(boardstate, side):
    return (boardstate == side).all(0).any()

def are_winning_cols(boardstate, side):
    return (boardstate == side).all(1).any()

def are_winning_diags(boardstate, side):
    return (boardstate.diagonal() == side).all() or \
           (nm.fliplr(boardstate).diagonal() == side).all()

def is_winner(boardstate, side):
    """
    Takes board.state matrix, side to check, returns if winner.  A player can
    only win after his own turn, so only checks one side at a time.
    """
    winner = False # no winner/draw yet
    if are_winning_rows(boardstate, side) or \
       are_winning_cols(boardstate, side) or \
       are_winning_diags(boardstate, side):
        winner = True
    return winner

def is_draw(boardstate):
    """
    Just sees if the board is full.  You have to call this after is_winner.
    """
    return nm.all(boardstate != 0)


class StateValues:
    """
    Dictionary like structure that maps hashes of board states to
    probabilities.  __setitem__ should not normally be used.
    
    When using __getitem__, if a boardstate hasn't been seen before: for a
    winning state, a probability of 1 is set before returning, for a losing
    state, a probability of 0 is set before returning, and for any other
    unknown state, a value of `default_value` is set before returning.
    """
    def __init__(self, side, default_value=0.5):
        self.data = {}
        self.side = side 
        if self.side == X:
            self.opponent = O
        else:
            self.opponent = X

        self.default_value = default_value

    def __repr__(self):
        return self.data.__repr__()

    def __len__(self):
        return self.data.__len__()

    def __setitem__(self, boardstate, value):
        self.data[str(boardstate)] = value

    def __getitem__(self, boardstate):
        if self.data.has_key(boardstate):
            pass
        elif is_winner(boardstate, self.side):
            self.data[str(boardstate)] = 1
        elif (is_winner(boardstate, self.opponent) or
              is_draw(boardstate)):
            self.data[str(boardstate)] = 0
        else: # state hasn't been seen and isn't a winner
            self.data[str(boardstate)] = self.default_value
        return self.data[str(boardstate)]


class Player():
    """Tic-tac-toe player"""
    def __init__(self, side, board=None,
            default_value=0.5,
            epsilon=0.1,
            alpha=0.9,
            learn_while_exploring=False):
        """Initialize player.

        board := instance of Board class
        side := X or O
        default_value := probability returned by value function for unexplored
            states
        epsilon := probability of exploration, (epsilon for
            e-greedy algorithm)
        alpha := learning rate (alpha)
        """
        self.board = board # tic-tac-toe board
        self.side = side # X or O

        # Values are probabilites between 0 and 1.  Set value of winning
        # board states to 1, losing states to 0.
        self.state_values = StateValues(side, default_value)
        self.exploration_rate = epsilon
        self.learning_rate = alpha
        self.learn_while_exploring = learn_while_exploring

        # Record
        self.record = {
            'Games': 0,
            'Wins': 0,
            'Losses': 0,
            'Draws': 0,
            'States Seen': 0
            }

    def __repr__(self):
        return Board.rep[self.side]

    def value(self, position):
        """
        Return probability of winning if 'position' is the next play made
        """ 
        test_board = self.board.state.copy()
        test_board[position[0], position[1]] = self.side
        return self.state_values[test_board]

    def new_game(self, board):
        """Reset board"""
        self.board = board

    def learn(self, chosen_value):
        """Update state value based on chosen state value"""
        self.state_values[self.board.state] += self.learning_rate * \
                (chosen_value - self.state_values[self.board.state])

    def play(self):
        """
        Evaluate choices and make a move.  Update state values.
        """
        def _find(mat): return [p[0] for p in
                nm.transpose(nm.nonzero(mat)).tolist()]

        open_positions = _find(self.board.state == BLANK)
        if self.exploration_rate < 1: # efficiency hack
            values = [self.value(p) for p in open_positions]
        
        if random.random() < self.exploration_rate: # explore
            chosen_position = random.sample(open_positions, 1)[0]
                                              # efficiency hack
            if self.learn_while_exploring and self.exploration_rate < 1:
                self.learn(self.value(chosen_position))
        else: # greedy
            chosen_value = max(values)
            # since multiple choices could be equally greedy, we need to
            # randomly select among them
            greedy_positions = [pos for (pos, value) in enumerate(values) if
                    value == chosen_value]
            chosen_position = open_positions[random.sample(greedy_positions, 1)[0]]
            self.learn(chosen_value)

        self.board.play(self.side, chosen_position)


def take_turn(player, board, pause, view):
    player.play()
    if view: 
        print board
        if pause: 
            raw_input()
        else:
            print ""

def simulate_game(p1, p2, pause=False, view=False):
    board = Board()
    p1.new_game(board)
    p2.new_game(board)
    player = itertools.cycle((p1, p2))

    # simulation loop
    while True:
        p = player.next()
        take_turn(p, board, pause, view)
        p.record['States Seen'] = len(p1.state_values)
        if is_winner(board.state, p.side):
            p.record['Wins'] += 1
            player.next().record['Losses'] += 1
            if view: 
                print p, "wins!"
            break
        elif is_draw(board.state):
            p1.record['Draws'] += 1
            p2.record['Draws'] += 1
            if view: 
                print "Game is a draw."
            break

    p1.record['Games'] += 1
    p2.record['Games'] += 1
    return

def simulate_series(p1, p2, ngames):
    for _ in xrange(ngames):
        simulate_game(p1, p2)
        yield (p1, p2)



###############################################################################
# Run and plot experiments
###############################################################################

def run_experiment_decreasing_epsilon(ngames, nruns=1):
    runs = []
    for _ in xrange(nruns):
        # wins versus random player
        p1 = Player(X, epsilon=0.9, learn_while_exploring=False)
        p2 = Player(O, epsilon=1, learn_while_exploring=False)
        results = []
        for _ in xrange(ngames):
            (p1, p2) = simulate_series(p1, p2, ngames).next()
            p1.exploration_rate *= 0.99
            results.append((p1.record['Wins'], p2.record['Wins']))
        runs.append(results)
    return runs

def run_experiment(ngames=10, nruns=1, statistic='Wins', default_value=0.5, 
        epsilon_X=0.1, alpha_X=0.9, learn_while_exploring_X=True, 
        epsilon_O=0.1, alpha_O=0.9, learn_while_exploring_O=True):

    runs = []
    for _ in xrange(nruns):
        p1 = Player(X, epsilon=epsilon_X, alpha=alpha_X,
                learn_while_exploring=learn_while_exploring_X)
        p2 = Player(O, epsilon=epsilon_O, alpha=alpha_O,
                learn_while_exploring=learn_while_exploring_O)

        runs.append([(x.record[statistic], o.record[statistic]) for (x, o) in
            simulate_series(p1, p2, ngames)])

    return runs

def avg(results):
    """Averages results from several runs."""

    xwins = [zip(*result)[0] for result in results]
    owins = [zip(*result)[1] for result in results]

    xwins_avg = np.average(np.array(xwins), 0)
    owins_avg = np.average(np.array(owins), 0)

    return zip(xwins_avg, owins_avg)

def make_report(nruns=5, ngames=100):
    """Generate and save all the plots for the report"""

    figdir = path.join('report', 'figures')
    run = partial(run_experiment, ngames=ngames, nruns=nruns)
    colors = itertools.cycle(('b','g','r','c','m','y','k'))

    def save_pdf(name):
        plt.savefig(path.join(figdir, name + '.pdf'))

    def label_wins_v_games():
        plt.figure()
        plt.xlabel('Games')
        plt.ylabel('Wins')

    def extended_title(title, epsilon_X, epsilon_O):
        plt.title(title + '\n' + \
                '$\epsilon_X = ' + str(epsilon_X) + '$,' + \
                '$\epsilon_O = ' + str(epsilon_O) + '$')

    def publish_fixed_epsilon_paths(title, epsilon_X, epsilon_O):
        """Higher order function to run and plot experiment runs"""
        label_wins_v_games()
        extended_title(title, epsilon_X, epsilon_O)
        plt.hold = True
        [plt.plot(p, colors.next()) for p in run(epsilon_X=1, epsilon_O=1)]
        plt.hold = False
        save_pdf(title)

    def publish_fixed_epsilon_avg(title, epsilon_X, epsilon_O):
        """Higher order function to run and plot average of experiment runs"""
        run_avg = avg(run(epsilon_X=epsilon_X, epsilon_O=epsilon_O))
        label_wins_v_games()
        extended_title(title, epsilon_X, epsilon_O)
        plt.plot(run_avg)
        plt.legend(('X','O'), loc='upper left')
        save_pdf(title)

    def publish_multi_epsilon(title, statistic='Wins'):
        eps = np.arange(0.1, 0.6, 0.1)
        data = [avg(run_experiment(ngames=ngames, nruns=nruns,
            statistic=statistic, epsilon_X=e, epsilon_O=1)) for e in eps]
        plt.figure()
        plt.xlabel('Games')
        plt.ylabel(statistic)
        plt.title(title)
        [plt.plot(zip(*p)[0]) for p in data]
        plt.legend(eps, loc='upper left')
        save_pdf(title + statistic)

    def publish_decreasing_epsilon(title):
        run_avg = avg(run_experiment_decreasing_epsilon(ngames, nruns))
        label_wins_v_games()
        plt.title(title)
        plt.plot(run_avg)
        plt.legend(('X', 'O'), loc='upper left')
        save_pdf(title)


    publish_fixed_epsilon_paths("Random Player vs. Random Player, All Paths",
            epsilon_X=1, epsilon_O=1)
    publish_fixed_epsilon_avg('Random Player vs. Random Player',
            epsilon_X=1, epsilon_O=1)
    publish_fixed_epsilon_avg('Learner vs. Random Player',
            epsilon_X=0.1, epsilon_O=1)
    publish_fixed_epsilon_avg('Random Player vs. Learner',
            epsilon_X=1, epsilon_O=0.1)
    publish_fixed_epsilon_avg('Learner vs. Learner',
            epsilon_X=0.1, epsilon_O=0.1)
    publish_multi_epsilon('Learner vs. Random Player, Varying $\epsilon$',
            statistic='Wins')
    publish_multi_epsilon('Learner vs. Random Player, Varying $\epsilon$',
            statistic='States Seen')
    publish_decreasing_epsilon('Learner vs. Random Player,' + \
            'Decreasing $\epsilon$ over time')


if __name__ == '__main__':
    make_report(nruns=5, ngames=10000)

 

###############################################################################
# Tests
###############################################################################

def test_board_states():
    # board state tests
    b = Board()
    pX = Player(X,b)
    pO = Player(O,b)

    b.state = nm.matrix("1 0 0; 1 1 1; 1 0 0")
    assert(are_winning_rows(b.state, X) and are_winning_cols(b.state, X))
    assert(is_winner(b.state, pX.side))

    b.state = nm.matrix("2 2 2; 0 0 2; 1 0 2")
    assert(are_winning_rows(b.state, O) and are_winning_cols(b.state, O))
    assert(is_winner(b.state, pO.side))

    b.state = nm.matrix("1 0 0; 0 1 0; 0 0 1")
    assert(are_winning_diags(b.state, X))
    assert(is_winner(b.state, pX.side))

    b.state = nm.matrix("0 0 1; 0 1 0; 1 0 0")
    assert(are_winning_diags(b.state, X))
    assert(is_winner(b.state, pX.side))

    b.state = nm.matrix("0 0 1; 0 1 0; 1 0 0")
    assert(are_winning_diags(b.state, X))
    assert(is_winner(b.state, pX.side))

    b.state = nm.matrix("1 1 2; 2 2 1; 1 1 2")
    assert(not are_winning_diags(b.state, X) and
           not are_winning_rows(b.state, O) and
           not are_winning_cols(b.state, O))
    assert(not is_winner(b.state, pX.side))
    assert(not is_winner(b.state, pO.side))
    assert(is_draw(b.state))

    b.state = nm.matrix("1 1 1; 2 2 1; 2 2 1")
    assert(is_winner(b.state, pX.side))
    assert(not is_winner(b.state, pO.side))

    b.state = nm.matrix("1 2 1; 2 2 1; 2 2 1")
    assert(is_winner(b.state, pX.side))
    assert(is_winner(b.state, pO.side))

    b.state = nm.matrix("1 1 2; 2 2 1; 1 2 1")
    assert(not is_winner(b.state, pX.side))
    assert(not is_winner(b.state, pO.side))
    assert(is_draw(b.state))

    b.state = nm.matrix("2 1 1; 1 2 2; 1 2 1")
    assert(not is_winner(b.state, pX.side))
    assert(not is_winner(b.state, pO.side))
    assert(is_draw(b.state))


def test_state_values():
    # StateValues tests
    sv = StateValues(X)
    assert(sv[nm.matrix('1 2 1; 0 0 0; 0 0 0')] == 0.5)
    assert(sv[nm.matrix('1 2 1; 0 0 0; 0 0 0')] == 0.5)
    assert(sv[nm.matrix('1 1 1; 0 0 0; 0 0 0')] == 1)
    assert(sv[nm.matrix('0 1 0; 0 1 0; 0 1 0')] == 1)
    assert(sv[nm.matrix('0 0 2; 0 2 0; 2 0 0')] == 0)


def test_simulate_game(ngames=1000):
    pX = Player(X)
    pO = Player(O, epsilon=1)
    for _ in xrange(ngames):
        simulate_game(pX, pO, pause=False, view=False)
        assert(pX.record['Games'] == sum((pX.record['Wins'], 
                                          pX.record['Draws'],
                                          pX.record['Losses'])))
        assert(pO.record['Games'] == sum((pO.record['Wins'], 
                                          pO.record['Draws'],
                                          pO.record['Losses'])))
        assert(pO.record['Games'] == pX.record['Games'])
        assert(pO.record['Wins'] == pX.record['Losses'])
        assert(pO.record['Losses'] == pX.record['Wins'])
        assert(pO.record['Draws'] == pX.record['Draws'])

def run_tests():
    test_board_states()
    test_state_values()
    test_simulate_game()
