#!/usr/bin/env python
"""
This example demonstrates how to use the discrete Temporal Difference
Reinforcement Learning algorithms (SARSA, Q, Q(lambda)) in a classical
fully observable MDP maze task. The goal point is the top right free
field. 

Derived from the PyBrain example by Thomas Rueckstiess.

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

from scipy import *
import sys, time
import pylab

from pybrain.rl.environments.mazes import Maze, MDPMazeTask
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, QLambda, SARSA #@UnusedImport
from pybrain.rl.explorers import BoltzmannExplorer #@UnusedImport
from pybrain.rl.experiments import Experiment
from pybrain.rl.environments import Task


# create the maze with walls (1)
envmatrix = array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 0, 1, 0, 1],
                   [1, 0, 0, 1, 0, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]])


#pylab.pcolor(envmatrix)
#pylab.draw()


def plotMaze():
    pylab.pcolor(envmatrix)
    pylab.title("Maze")


def initExperiment(alg, optimistic=True):
    env = Maze(envmatrix, (7, 7))

    # create task
    task = MDPMazeTask(env)

    # create value table and initialize with ones
    table = ActionValueTable(81, 4)
    if optimistic:
        table.initialize(1.)
    else:
        table.initialize(0.)

    # create agent with controller and learner - use SARSA(), Q() or QLambda() here
    learner = alg()

    # standard exploration is e-greedy, but a different type can be chosen as well
    # learner.explorer = BoltzmannExplorer()

    agent = LearningAgent(table, learner)
    agent.batchMode = False

    experiment = Experiment(task, agent)
    experiment.allRewards = []
    return experiment


def doExperiment(experiment, N):
    # alpha=0.5, gamma=0.99, lambda=0.9
    for i in range(N):
        # interact with the environment
        experiment.doInteractions(1)
        experiment.agent.learn()
        experiment.allRewards.append(experiment.agent.lastreward)
        if not(experiment.agent.learner.__class__.__name__ == 'QLambda'):
            experiment.agent.reset()
    print "Run %d completed" % (experiment.stepid,)

def doEpisode(experiment):
    while True:
        experiment.doInteractions(1)
        experiment.agent.learn()
        if experiment.agent.lastreward:
            break
        if not(experiment.agent.learner.__class__.__name__ == 'QLambda'):
            experiment.agent.reset()
    if not(experiment.agent.learner.__class__.__name__ == 'QLambda'):
        experiment.agent.reset()
    experiment.doInteractions(1)
    experiment.agent.learn()
    experiment.agent.reset()


def doExperiments(experiments, N):
    for e in experiments:
        doExperiment(e, N)


def doFullExperiment(N, repetitions):
    # runs R sets of experiments and averages them
    algs = [SARSA, Q, QLambda]
    fullData = []
    for _ in range(repetitions):
        experiments = map(initExperiment, algs)
        doExperiments(experiments, N)
        fullData.append(experiments)
    return fullData

def averageRewards(fullData):
    nreps = len(fullData)
#    nruns = len(fullData[0][0].agent.history.data['reward'])
    nruns = len(fullData[0][0].allRewards)
    sarsaData = pylab.zeros((nreps, nruns))
    QData = pylab.zeros((nreps, nruns))
    QLambdaData = pylab.zeros((nreps, nruns))
    for (index, rep) in enumerate(fullData):
#        sarsaData[index] = rep[0].agent.history.data['reward'].T
#        QData[index] = rep[1].agent.history.data['reward'].T
#        QLambdaData[index] = rep[2].agent.history.data['reward'].T
        sarsaData[index] = rep[0].allRewards
        QData[index] = rep[1].allRewards
        QLambdaData[index] = rep[2].allRewards
    return [cumsum(data,1).mean(0) for data in [sarsaData, QData, QLambdaData]]


def plotAVTable(experiment):
    pylab.figure()
    pylab.gray()
    pylab.pcolor(experiment.agent.module.params.reshape(81,4).max(1).reshape(9,9),
            shading='faceted')
    pylab.title("Action-Value table, %s, Run %d" %
            (experiment.agent.learner.__class__.__name__, experiment.stepid))

def plotReward(experiment):
    pylab.plot(cumsum(experiment.agent.history.data['reward']),
            label=experiment.agent.learner.__class__.__name__)

def plotRewards(experiments):
    pylab.figure()
    for e in experiments:
        plotReward(e)
    pylab.title("Cumulative reward, %d interactions" % (experiments[0].stepid,))
    pylab.legend()

def plotAverageRewards(averageRewards, nreps):
    pylab.figure()
    pylab.plot(averageRewards[0], label='SARSA')
    pylab.plot(averageRewards[1], label='Q')
    pylab.plot(averageRewards[2], label='QLambda')
    pylab.title("Average cumulative reward, %d interactions, %d repetitions" %
            (averageRewards[0].shape[0], nreps))
    pylab.legend(loc='upper left')
