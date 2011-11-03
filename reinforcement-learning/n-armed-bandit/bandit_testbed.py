#! /usr/bin/env python

"""
Functions for experimenting with reinforcement learning in n-armed
bandits.

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

from __future__ import division, print_function

import numpy as np
import functools
import collections
from matplotlib import pyplot


def multimax(lst):
    """
    Return the tuple (maxvalue, maxindex).  If there is more than one max
    value, return one of them randomly.
    """
    maxvalue = np.max(lst)
    maxindices = np.flatnonzero(lst == maxvalue)
    random_index = np.random.randint(len(maxindices))
    return (maxvalue, maxindices[random_index])


class BanditTestbed:

    def __init__(self, narms, variance=1):
        self.narms = narms
        self.variance = variance
        self.mean_rewards = np.random.standard_normal(narms)

    def __str__(self):
        return 'narms = {0}\nmean_rewards = {1}'.format(self.narms,
                self.mean_rewards)

    def play(self, arm):
        assert(arm in range(self.narms))
        if self.variance == 0:
            reward = self.mean_rewards[arm]
        else:
            reward = np.random.normal(self.mean_rewards[arm],
                    np.sqrt(self.variance))
        return reward


class Player:

    def __init__(self, testbed, factor=0.1, initial_estimates=0):
        self.testbed = testbed
        self.mean_estimates = np.zeros(testbed.narms) + initial_estimates
        self.npulls = np.zeros(testbed.narms)
        self.reward_record = []
        self.pull_record = []
        self.factor = factor

    def __str__(self):
        return 'mean_estimates = {0}'.format(self.mean_estimates)

    def choose_arm(self):
        # need to implement
        pass

    def play(self):
        arm = self.choose_arm()
        reward = self.testbed.play(arm)
        self.pull_record.append(arm)
        self.reward_record.append(reward)

        # incremental sample averaging
        self.mean_estimates[arm] += (1/(self.npulls[arm] + 1)) * (reward -
                self.mean_estimates[arm])

        self.npulls[arm] += 1


class EpsilonPlayer(Player):

    factor_name = r'\epsilon'

    def __init__(self, testbed, factor=0.1, initial_estimates=0):
        Player.__init__(self, testbed, factor,
                initial_estimates=initial_estimates)

    def choose_arm(self):
        if np.random.uniform() < self.factor: # explore
            arm = np.random.randint(self.testbed.narms)
        else: # greedy
            value, arm = multimax(self.mean_estimates)
        return arm


def random_weighted(weights):
    cumulative_weights = np.cumsum(weights)
    cdf = cumulative_weights / cumulative_weights[-1]
    return cdf.searchsorted(np.random.uniform())


class SoftmaxPlayer(Player):

    factor_name = r'\tau'

    def __init__(self, testbed, factor=0.1, initial_estimates=0):
        Player.__init__(self, testbed, factor=factor,
                initial_estimates=initial_estimates)

    def choose_arm(self):
        N = np.exp(self.mean_estimates / self.factor)
        return random_weighted(N)


def do_experiment(PlayerClass=EpsilonPlayer, ntasks=2000, narms=10,
        nplays=1000, factor=0.1, variance=1):

    def task(n):
        if n % 100 == 0:
            print(PlayerClass.factor_name + ':', factor, 'Task:', n, 'started')
        testbed = BanditTestbed(narms, variance)
        player = PlayerClass(testbed, factor=factor)
        for j in xrange(nplays):
            player.play()
        return player

    return [task(n) for n in xrange(ntasks)]


def mean_reward(players):
    rewards = np.vstack(p.reward_record for p in players)
    return rewards.mean(0)


def optimal_pull(player):
    return np.argmax(player.testbed.mean_rewards)

def optimal_counts(players):
    pull_matrix = np.vstack(p.pull_record for p in players)
    ntasks, nplays = pull_matrix.shape
    optimal_plays = [optimal_pull(p) for p in players]
    optimal_column = np.reshape(optimal_plays, (ntasks, 1))
    assert(optimal_column.shape == (ntasks, 1))
    optimal_matrix = np.tile(optimal_column, (1, nplays))
    assert(optimal_matrix.shape == (ntasks, nplays))
    optimal_count = np.sum((pull_matrix == optimal_matrix), 0)
    assert(optimal_count.size == nplays)
    return (optimal_count, ntasks)

def percent_optimal_action(players):
    noptimal, ntasks = optimal_counts(players)
    return 100 * noptimal / ntasks


## Tests

def test_multimax():
    foo = np.array([1, 2, 3, 4, 5, 6])
    assert(multimax(foo) == (6, 5))

    foo = np.array([1, 6, 3, 6, 5, 3])
    (rvalue, rindex) = multimax(foo)
    print(rindex)
    assert(rvalue == 6)
    assert(rindex == 1 or rindex == 3)
    (rvalue, rindex) = multimax(foo)
    print(rindex)
    assert(rindex == 1 or rindex == 3)


def test_random_weighted():
    val_gen = random_weighted(range(10))
    vals = [val_gen.next() for x in range(100)]
    assert((0 <= vals <= 1).all())


## Recreate Figure 2.1 from Sutton and Barto with several experiments

def experiment_2_1(PlayerClass=EpsilonPlayer, ntasks=2000, nplays=1000,
        variance=1, factors=(0, 0.01, 0.1, 0.5)):
    experiment = functools.partial(do_experiment, PlayerClass=PlayerClass,
            ntasks=ntasks, narms=10, nplays=nplays, variance=variance)
    results = collections.OrderedDict([(f, experiment(factor=f)) for f in factors])
    return results

def plot_2_1(results):
    fig, (ax1, ax2) = pyplot.subplots(2,1, sharex=True, sharey=False)
    fig.hold(True)
    for factor in results:
        factor_name = results[factor][0].factor_name
        ax1.plot(mean_reward(results[factor]), 
                label=r'${0}={1}$'.format(factor_name, factor))
        ax2.plot(percent_optimal_action(results[factor]),
                label=r'${0}={1}$'.format(factor_name, factor))

    ax1.set_yticks(np.arange(0, 1.6, 0.5))
    ax1.set_ylabel('Average reward')
    leg1 = ax1.legend(loc='lower right', fancybox=True, labelspacing=0)
    leg1.get_frame().set_alpha(0.5)

    ax2_yticks = range(0, 101, 20)
    ax2.set_yticks(ax2_yticks)
    ax2.set_yticklabels([str(tick) + '%' for tick in ax2_yticks])
    ax2.set_ylabel('% Optimal action')
    ax2.set_xlabel('Plays')
    leg2 = ax2.legend(loc='lower right', fancybox=True, labelspacing=0)
    leg2.get_frame().set_alpha(0.5)

    return fig


experiment_exercise_2_1 = functools.partial(experiment_2_1, nplays=5000)
experiment_high_variance = functools.partial(experiment_2_1, variance=10)
experiment_no_variance = functools.partial(experiment_2_1, variance=0)
experiment_exercise_2_2 = functools.partial(experiment_2_1,
        PlayerClass=SoftmaxPlayer, 
        factors=(0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1))
