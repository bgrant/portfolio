#! /usr/bin/env python

"""
Experiments with learning the optimal strategy for playing blackjack
using reinforcement learning.  Starts from examples 5.1 and 5.3 from
Sutton and Barto

:author: Robert Grant <bgrant@mail.utexas.edu>

:copyright:
    Copyright 2011 Robert Grant

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

from __future__ import division, print_function
import numpy as np
import itertools
import matplotlib
matplotlib.use('PDF')
from matplotlib import pyplot


class Const:
    ACE = 1
    HIT, STICK = (0, 1)
    USABLE_ACE, CURRENT_SUM, DEALER_SHOWING, ACTIONS = (0, 1, 2, 3)
    STATE_RANGES = [(0, 2), (12, 22), (1, 11), (0, 2)]


def multimax(lst):
    """
    Return the tuple (maxvalue, maxindex).  If there is more than one max
    value, return one of them randomly.
    """
    maxvalue = np.max(lst)
    maxindices = np.flatnonzero(lst == maxvalue)
    random_index = np.random.randint(len(maxindices))
    return (maxvalue, maxindices[random_index])


def random_weighted(weights):
    """
    Given a list of (not-necessarily normalized) weights, return an
    index into the list with probability proportional to each weight.
    """
    cumulative_weights = np.cumsum(weights)
    cdf = cumulative_weights / cumulative_weights[-1]
    return cdf.searchsorted(np.random.uniform())


def random_card():
    """
    Return value a random card, with each card weighted to it's proper
    probability of occurring
    """
    #               A  2  3  4  5  6  7  8  9  10
    card_weights = [4, 4, 4, 4, 4, 4, 4, 4, 4, 16]
    return random_weighted(card_weights) + 1


def test_random_card():
    cards = np.array([random_card() for x in xrange(1000)])
    assert((1 <= cards).all())
    assert((cards <= 10).all())
    for x in xrange(1, 10):
        assert(cards.tolist().count(10) > cards.tolist().count(x))


def ind(tup):
    return tuple([i] for i in tup)


class Dealer:
    """
    Blackjack dealer
    """
    def __init__(self):
        self.showing_card = None
        self.current_sum = None
        self.naces = 0

    def update_current_sum(self, card):
        if card == Const.ACE:
            self.naces += 1
        self.current_sum += card
        if is_busted(self) and self.naces > 0:
            self.current_sum -= 10
            self.naces -= 1

    def new_game(self, showing_card):
        self.current_sum = 0
        self.showing_card = showing_card
        self.update_current_sum(showing_card)

    def play_game(self):
        """
        Play with fixed strategy: hit until current_sum >= 17.  Treat aces as
        11 unless bust, then treat as 1
        """
        while self.current_sum < 17:
            next_card = random_card()
            self.update_current_sum(next_card)

def test_Dealer():
    for x in xrange(100):
        d = Dealer()
        d.new_game(np.random.randint(1,11))
        assert(1 <= d.showing_card <= 10)
        d.play_game()
        assert(17 <= d.current_sum <= 26)


class Player:
    """
    Blackjack player to find the optimal blackjack policy, using
    monte-carlo exploring-starts.
    """

    def __init__(self, es_strategy):
        """
        self.Q is the computed state-action values, a floating-point
        value from -1 to 1, represented as a 4-D array with dimensions

            usable_ace   current_sum  dealer_showing  action
            -------------------------------------------------
                 2     x      22     x     11        x   2


            State/Action     Real Value       Index
            ------------------------------------------
            usable_ace       {True, False}    {0, 1}
            current_sum      {12-21}          {12..21}
            dealer_showing   {A-10}           {1..10}
            actions          {hit, stick}     {0, 1}

        Q table is made larger than necessary to simplify indexing, i.e.
        lower part of current_sum is never used

        self.policy is a 3-D array, with dimensions equal to the first
        three dimensions of self.Q
        """
        self.Q = np.zeros([t[-1] for t in Const.STATE_RANGES])
        self.Q_count = np.zeros(self.Q.shape, int)
        self.policy = np.zeros(self.Q.shape[0:-1], int)
        self.policy[:, [20, 21], :] = Const.STICK # stick on 20 and 21 initially
        self.dealer = Dealer()
        self.current_sum = None
        self.states = None
        self.nepisodes = 0

        if es_strategy == 'all_pairs': # enumerate all start state-action pairs
            self.next_state = itertools.cycle(itertools.product(*[xrange(*t)
                for t in Const.STATE_RANGES]))
        elif es_strategy == 'rnd_pairs': # start with a random start state-action pair
            self.next_state = self.random_pairs()
        elif es_strategy == 'rnd_states': # start with a random state only
            self.next_state = self.random_states()
        else:
            assert(0)

    def random_pairs(self):
        while True:
            yield tuple(np.random.randint(*t) for t in Const.STATE_RANGES)

    def random_states(self):
        while True:
            state = tuple(np.random.randint(*t) for t in
                    Const.STATE_RANGES[:-1]) 
            yield state + (self.policy[state],)

    def play_game(self):
        """
        Play through a game of blackjack, starting in a random or
        enumerated state
        """
        # choose starting state-action pair
        next_pair = self.next_state.next()
        start_state = tuple(next_pair[:3])
        action = next_pair[-1]

        # initialize record-keeping
        self.states = [start_state]
        self.actions = [action]
        self.dealer.new_game(start_state[Const.DEALER_SHOWING])
        self.current_sum = self.states[-1][Const.CURRENT_SUM]

        while (not is_busted(self) and action == Const.HIT):
#                self.policy[self.states[-1]] == Const.HIT): # first try
            self.current_sum = self.states[-1][Const.CURRENT_SUM] + random_card()
            if not is_busted(self):
                next_state = (self.states[-1][Const.USABLE_ACE],
                              self.current_sum,
                              self.states[-1][Const.DEALER_SHOWING])
                self.states.append(next_state)
                action = self.policy[self.states[-1]]
                self.actions.append(action)
            elif self.states[-1][Const.USABLE_ACE]: # busted, but usable ace
                self.current_sum -= 10
                next_state = (0,
                              self.current_sum,
                              self.states[-1][Const.DEALER_SHOWING])
                self.states.append(next_state)
                action = self.policy[self.states[-1]]
                self.actions.append(action)
            #else: busted and nothing to do about it
        self.nepisodes += 1

    def update_Q(self, reward):
        """
        Incrementally update each visted state with reward from game outcome
        """
        for state, action in zip(self.states, self.actions):
            Q_index = state + (action,)
            self.Q_count[Q_index] += 1
            self.Q[Q_index] += (1/self.Q_count[Q_index]) * (reward - self.Q[Q_index])

    def update_policy(self):
        """
        Set the new policy to be the action leading to the highest value
        from every visited state
        """
        for state in self.states:
            self.policy[state] = multimax(self.Q[state])[1]

    def run_episode(self):
        """
        Generate a monte carlo episode.
        """
        self.play_game()
        self.dealer.play_game()
        self.update_Q(compute_reward(self, self.dealer))
        self.update_policy()

    def counts(self, usable, action):
        """
        Return the times each state has been visted.
        """
        current_sum_range = Const.STATE_RANGES[Const.CURRENT_SUM]
        dealer_showing_range = Const.STATE_RANGES[Const.DEALER_SHOWING]
        return self.Q_count[usable, current_sum_range[0]:,
                dealer_showing_range[0]:, action]


def is_busted(player):
    if player.current_sum > 21:
        busted = True
    else:
        busted = False
    return busted


def compute_reward(player, dealer):
    """
    Return reward based on who won
    """
    if is_busted(player) and is_busted(dealer): # draw
        reward = 0
    elif is_busted(player) and not is_busted(dealer): # lose
        reward = -1
    elif is_busted(dealer) and not is_busted(player): # win
        reward = 1
    # no one busted
    elif player.current_sum == dealer.current_sum: # draw
        reward = 0
    elif player.current_sum < dealer.current_sum: # lose
        reward = -1
    elif player.current_sum > dealer.current_sum: # win
        reward = 1
    else:
        assert False
    return reward

def test_compute_reward():
    d = Dealer()
    p = Player(d)

    for reverse in [False, True]:
        for dealer_sum in range(1,22):
            d.current_sum = dealer_sum
            for player_sum in (range(dealer_sum) + range(22,33)):
                p.current_sum = player_sum
                if reverse:
                    p.current_sum = dealer_sum
                    d.current_sum = player_sum
                r = compute_reward(p, d)
                print(d.current_sum, p.current_sum, r)
                if reverse:
                    assert r == 1
                else:
                    assert r == -1

    for i in range(33):
        d.current_sum = i
        p.current_sum = i
        r = compute_reward(p, d)
        print(d.current_sum, p.current_sum, r)
        assert r == 0


def plot_blackjack(player, plot_type, action=0):
    """
    Generate a diagram of player's policy or a heatmap of player's value
    function or a heatmap of the number of times each state-action has
    been visited.
    """
    fig, (ax1, ax2) = pyplot.subplots(2,1, sharex=True, sharey=True)
    fig.hold(True)
    current_sum_range = range(*Const.STATE_RANGES[Const.CURRENT_SUM])
    dealer_showing_range = range(*Const.STATE_RANGES[Const.DEALER_SHOWING])
    dealer_showing_labels = ['A',] + dealer_showing_range[1:]

    ax1.set_ylabel('Usable ace')
    ax1.set_yticks(np.arange(0.5, 9.6, 1))
    ax1.set_yticklabels('')
    ax1_2 = ax1.twinx()
    ax1_2.set_ylabel('Player Sum')
    ax1_2.set_yticks(np.arange(0.5, 9.6, 1))
    ax1_2.set_yticklabels(current_sum_range)

    ax2.set_ylabel('No usable ace')
    ax2.set_yticks(np.arange(0.5, 9.6, 1))
    ax2.set_yticklabels('')
    ax2_2 = ax2.twinx()
    ax2_2.set_ylabel('Player Sum')
    ax2_2.set_yticks(np.arange(0.5, 9.6, 1))
    ax2_2.set_yticklabels(current_sum_range)
    ax2_2.set_xlabel('Dealer showing')
    ax2_2.set_xticks(np.arange(0.5, 9.6, 1))
    ax2_2.set_xticklabels(dealer_showing_labels)

    if plot_type == 'policy':
        ax1_2.pcolor(player.policy[1, current_sum_range[0]:, dealer_showing_range[0]:])
        ax2_2.pcolor(player.policy[0, current_sum_range[0]:, dealer_showing_range[0]:])
    elif plot_type == 'value':
        max_usable = player.Q[1, current_sum_range[0]:,
                dealer_showing_range[0]:].max(2)
        max_no_usable = player.Q[0, current_sum_range[0]:,
                dealer_showing_range[0]:].max(2)
        ax1_2.pcolor(max_usable, cmap=pyplot.cm.hot)
        ax2_2.pcolor(max_no_usable, cmap=pyplot.cm.hot)
    elif plot_type == 'count':
        counts_usable = player.Q_count[1, current_sum_range[0]:,
                dealer_showing_range[0]:, action]
        counts_no_usable = player.Q_count[0, current_sum_range[0]:,
                dealer_showing_range[0]:, action]
        ax1_2.pcolor(counts_usable, cmap=pyplot.cm.hot)
        ax2_2.pcolor(counts_no_usable, cmap=pyplot.cm.hot)

    return fig, (ax1_2, ax2_2)



def all_plots(player, name):
    """
    Make all four plots and save them with the prefix `name`.
    """
    for f in ('policy', 'value'):
        fig, etc = plot_blackjack(player, f)
        fig.savefig('figures/{2}_after_{0}_{1}.pdf'.format(player.nepisodes, f,
            name))

    for f in zip((Const.HIT, Const.STICK), ('hit', 'stick')):
        fig, etc = plot_blackjack(player, 'count', f[0])
        fig.savefig('figures/{2}_after_{0}_counts_{1}.pdf'.format(player.nepisodes,
            f[1], name))

    for t in itertools.product(xrange(*Const.STATE_RANGES[Const.USABLE_ACE]), 
                               xrange(*Const.STATE_RANGES[Const.ACTIONS])):
        player.counts(*t).dump('figures/{3}_after_{0}_counts_{1}{2}.dump'.format(player.nepisodes,
            t[0], t[1], name)) 


def run_experiment(player, name, plot_points):
    for p in plot_points: 
        while player.nepisodes < p:
            if player.nepisodes % 5000 == 0:
                print(player.nepisodes)
            player.run_episode()
        all_plots(player, name) 
