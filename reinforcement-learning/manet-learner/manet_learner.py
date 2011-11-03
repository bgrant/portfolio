#!/usr/bin/env python

"""
Using reinforcement learning to switch routing algorithms based on
context in a MANET.

:copyright:
    Copyright 2011 Robert Grant and Agoston Petz

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

import numpy
import subprocess
import json
import pickle
import itertools
from matplotlib import pyplot

from pybrain.rl.environments.environment import Environment
from pybrain.rl.environments.task import Task
from pybrain.rl.learners.valuebased import ActionValueTable, ActionValueNetwork
from pybrain.rl.learners import Q, NFQ
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer


__author__ = 'Robert Grant, bgrant@mail.utexas.edu'
__author__ = 'Agoston Petz, agoston@mail.utexas.edu'


############
# Constants
############

sensorValues = ('load',
                'speed',
                'neighbors')

centerBinEdges_10s = ((12.194000, 273.562000),
                     (2.825204, 8.191208),
                     (4.000000, 10.000000))

centerBinEdges_30s = ((51.526000000000003, 4599.9499999999998),
                     (1.4519844525661101, 5.8436614618178098),
                     (5.0, 13.0))

centerBinEdges_10s_lessperturbed = ((10.326499999999999, 109.402),
                                    (4.5833993543897051, 5.3961982650487199),
                                    (3.0, 9.0))

rewardValues = ('throughput',
                'latency')

actions = ('DSDV', 'DYMOFAU')


#############
# Experiment 
#############


class OmnetEnvironment(Environment):

    def __init__(self, centerBinEdges, simscript='./mock_rlRunExperiment.pl',
            resetscript='./mock_rlResetExperiment.pl'):
        Environment.__init__(self)
        self.centerBinEdges = centerBinEdges
        self.data = []
        self.actions = []
        self.numErrors = 0
        self.simscript = simscript 
        self.resetscript = resetscript
        self.discreteStates = True
        self.discreteActions = True
        self.numActions = 2
        self.numSensors = len(sensorValues)
        if self.centerBinEdges is None:
            self.numSensorBins = 1
        else:
            self.numSensorBins = len(self.centerBinEdges[0]) + 1

    def getSensors(self):
        if self.data == []:
            return dict((name, value) for (name, value) in zip(sensorValues,
                numpy.zeros(len(sensorValues))))
        else:
            return self.data[-1]

    def performAction(self, action):
        self.runOmnetSimulation(action)

    def runOmnetSimulation(self, action):
        success = False
        while not(success):
            try:
                print("%s %s" % (self.simscript, action))
                jsonData = subprocess.Popen([self.simscript, action],
                                stdout=subprocess.PIPE).communicate()[0]
                self.data.append(json.loads(jsonData))
                self.actions.append(action)
                success = True
            except ValueError as details:
                self.numErrors += 1
                print("Error in data", details)
                print("Resetting simulation")
                subprocess.call(self.resetscript)


class OmnetTask(Task):
    def __init__(self, environment, centerBinEdges=None):
        self.env = environment
        self.centerBinEdges = centerBinEdges
        self.lastreward = 0
        self.allrewards = []

    def performAction(self, action):
        self.env.performAction(actions[int(action)])

    def getObservation(self):
        values = self.env.getSensors()
        if self.centerBinEdges is not None:
            values = self.binValues(rawValues)
            # linearize index
            values = numpy.array([self.linearizeIndex(binnedValues)])
        return values

    def linearizeIndex(self, binnedValues):
        binnedValues = [x for x in reversed(binnedValues)]
        index = 0
        for x in range(self.env.numSensors):
            index += (self.env.numSensors ** x) * binnedValues[x]
        return index

    def binValues(self, rawValues):
        assert(len(self.centerBinEdges[0]) == (self.env.numSensorBins - 1))
        indices = []
        for (value, edges) in zip(sensorValues, self.centerBinEdges):
            index = None
            if rawValues[value] < edges[0]:
                index = 0
            elif rawValues[value] > edges[1]:
                index = 2
            else:
                index = 1
            indices.append(index)
        return indices

    def getReward(self):
        """save current given reward and retrieve last reward"""
        current_reward = self.lastreward
        self.lastreward = self.env.data[-1]['throughput'] - \
                          1000*self.env.data[-1]['latency']
        self.allrewards.append(current_reward)
        return current_reward

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim


def initExperiment(learnalg='Q', history=None, binEdges='10s',
        scriptfile='./rlRunExperiment_v2.pl',
        resetscript='./rlResetExperiment.pl'):

    if binEdges == '10s':
        centerBinEdges = centerBinEdges_10s
    elif binEdges == '30s':
        centerBinEdges = centerBinEdges_30s
    elif binEdges == 'lessperturbed':
        centerBinEdges = centerBinEdges_10s_lessperturbed
    elif binEdges is None:
        centerBinEdges = None
    else:
        raise Exception("No bins for given binEdges setting")

    env = OmnetEnvironment(centerBinEdges, scriptfile, resetscript)
    if history is not None:
        env.data = history['data']

    task = OmnetTask(env, centerBinEdges)
    if history is not None:
        task.allrewards = history['rewards']

    if learnalg == 'Q':
        nstates = env.numSensorBins ** env.numSensors
        if history is None:
            av_table = ActionValueTable(nstates, env.numActions)
            av_table.initialize(1.)
        else:
            av_table = history['av_table']
        learner = Q(0.1, 0.9) # alpha, gamma
        learner._setExplorer(EpsilonGreedyExplorer(0.05)) # epsilon
    elif learnalg == 'NFQ':
        av_table = ActionValueNetwork(env.numSensors, env.numActions)
        learner = NFQ()
    else:
        raise Exception("learnalg unknown")

    agent = LearningAgent(av_table, learner)

    experiment = Experiment(task, agent)
    if history is None:
        experiment.nruns = 0
    else:
        experiment.nruns = history['nruns']
    return experiment


def runExperiment(experiment, nexperiments=1, datafile='experiment.dat'):
    nstates = experiment.task.env.numSensors ** experiment.task.env.numSensorBins
    nactions = experiment.task.env.numActions

    for x in xrange(nexperiments):
        experiment.doInteractions(1)
        experiment.agent.learn()
        experiment.agent.reset()
        experiment.nruns += 1

        if (x % 10 == 0) or (x == (nexperiments-1)):
            print("Run %s completed" % (experiment.nruns,))
            #plotAgent(experiment.agent.module, nstates, nactions)
            saveExperiment(experiment, datafile)


def saveExperiment(experiment, datafile='experiment.dat'):
    with open(datafile, 'w') as fh:
        print("Saving state...")
        pickle.dump({'av_table': experiment.agent.module,
                     'data': experiment.task.env.data,
                     'rewards': experiment.task.allrewards,
                     'actions': experiment.task.env.actions,
                     'nruns': experiment.nruns,
                     'nerrors': experiment.task.env.numErrors}, fh)


###########
# Analysis 
###########

def loadPickles(filename='./results_10s_lessperturbed_rl_run', nums=None):
    if nums is None:
        nums = range(1,6)

    pickles = []
    for x in nums:
        with open(filename + str(x) + '.pickle') as fh:
            pickles.append(pickle.load(fh))

    return pickles


def plotQTable(pickle, nstates=27, nactions=2):
    qtable = pickle['av_table'].params.reshape(nstates,nactions)
    pyplot.pcolor(qtable, cmap=pyplot.cm.gray)
    pyplot.title('Q Table')
    pyplot.xlabel('Action')
    pyplot.xticks((0.5, 1.5), ('DSDV', 'DYMOFAU'))
    pyplot.ylim([0,nstates])
    pyplot.yticks(numpy.arange(0.5, 27.5), 
            [reduce(lambda x, y: x + y, tup) for tup in itertools.product('012', repeat=3)])
#            [tup for tup in itertools.product('lmh', repeat=3)])
    pyplot.ylabel('State (Level of load,speed,neighbors)')
    pyplot.draw()


def stateActionCounts(pickle):
    tmap, fmatrix = makeFullMatrix([pickle])
    actions = numpy.array(pickle['actions']).reshape((1,-1)).T
    states = binSensors(tmap, fmatrix, centerBinEdges_10s_lessperturbed)
    states = states.reshape((-1,3))
    sa = numpy.hstack((states, actions))
    sa_rows = [tuple(sa[row, :].tolist()) for row in range(sa.shape[0])]
    sa_set  = set(sa_rows)
    counts = dict([(v, sa_rows.count(v)) for v in sa_set])

    ordered_states = itertools.product('012', repeat=3)
    qcounts = numpy.zeros((27,2))
    for s in ordered_states:
        row_index = (3**2)*int(s[0]) + 3*int(s[1]) + int(s[2])
        key = tuple([str(float(digit)) for digit in s])
        qcounts[row_index, 0] = counts[key + ('DSDV',)]
        qcounts[row_index, 1] = counts[key + ('DYMOFAU',)]
    return qcounts


def plotStateActionCounts(pickles):
    numpy.array([stateActionCounts(pickles[i]).sum(0) for i in range(2)])


def plotLoad(pickle, memory=10000, nstates=27, nactions=2):
    qtable = pickle['av_table'].params.reshape(nstates,nactions)
    qcounts = stateActionCounts(pickle)
    scaledqs = qtable[-memory:,:] * (qcounts[-memory:,:]/qcounts[-memory:,:].sum())
    newtable = numpy.zeros((nstates/9, nactions))
    newtable[0] = scaledqs[:9, :].sum(0)
    newtable[1] = scaledqs[9:18, :].sum(0)
    newtable[2] = scaledqs[18:, :].sum(0)
    pyplot.pcolor(newtable, cmap=pyplot.cm.gray)
    pyplot.title('Q Table')
    pyplot.xlabel('Action')
    pyplot.xticks((0.5, 1.5), ('DSDV', 'DYMOFAU'))
    pyplot.ylim([0,nstates/9])
    pyplot.yticks(numpy.arange(0.5, 2.6, 1), [0,1,2])
    pyplot.ylabel('State (Level of load)')
    pyplot.draw()


def plotSpeed(pickle, memory=10000, nstates=27, nactions=2):
    qtable = pickle['av_table'].params.reshape(nstates,nactions)
    qcounts = stateActionCounts(pickle)
    scaledqs = qtable[-memory:,:] * (qcounts[-memory:,:]/qcounts[-memory:,:].sum())
    newtable = numpy.zeros((nstates/9, nactions))
    newtable[0] = scaledqs[:3, :].sum(0) + scaledqs[9:12, :].sum(0) + scaledqs[18:21, :].sum(0)
    newtable[1] = scaledqs[3:6, :].sum(0) + scaledqs[12:15, :].sum(0) + scaledqs[21:24, :].sum(0)
    newtable[2] = scaledqs[6:9:, :].sum(0) + scaledqs[15:18, :].sum(0)+ scaledqs[24:27, :].sum(0)
    pyplot.pcolor(newtable, cmap=pyplot.cm.gray)
    pyplot.title('Q Table')
    pyplot.xlabel('Action')
    pyplot.xticks((0.5, 1.5), ('DSDV', 'DYMOFAU'))
    pyplot.ylim([0,nstates/9])
    pyplot.yticks(numpy.arange(0.5, 2.6, 1), [0,1,2])
    pyplot.ylabel('State (Level of speed)')
    pyplot.draw()


def plotNeighbors(pickle, memory=10000, nstates=27, nactions=2):
    qtable = pickle['av_table'].params.reshape(nstates,nactions)
    qcounts = stateActionCounts(pickle)
    scaledqs = qtable[-memory:,:] * (qcounts[-memory:,:]/qcounts[-memory:,:].sum())
    newtable = numpy.zeros((nstates/9, nactions))
    newtable[0] = scaledqs[range(0,27,3), :].sum(0)
    newtable[1] = scaledqs[range(1,27,3), :].sum(0)
    newtable[2] = scaledqs[range(2,27,3), :].sum(0)
    pyplot.pcolor(newtable, cmap=pyplot.cm.gray)
    pyplot.title('Q Table')
    pyplot.xlabel('Action')
    pyplot.xticks((0.5, 1.5), ('DSDV', 'DYMOFAU'))
    pyplot.ylim([0,nstates/9])
    pyplot.yticks(numpy.arange(0.5, 2.6, 1), [0,1,2])
    pyplot.ylabel('State (Level of n_neighbors)')
    pyplot.draw()


def getPolicy(pickles, nstates=27):
    agent_table = []
    for agent in pickles:
        agent_table.append([agent['av_table'].getMaxAction(state) for state in
            range(nstates)])
    tbl = numpy.array(agent_table)


def plotPolicy(pickles, nstates=27):
    tbl = getPolicy(pickles)
    nagents = len(pickles)
    pyplot.pcolor(tbl.T)
    pyplot.title('Policy After ' + str(pickles[0]['nruns']) + ' Runs\n DSDV=Blue, DYMOFAU=Red')
    pyplot.xticks(numpy.arange(0.5, nagents+0.5), range(1, nagents+2))
    pyplot.xlabel('Agent')
    pyplot.ylim([0, nstates])
    pyplot.ylabel('State (Level of load,speed,neighbors)')
    pyplot.yticks(numpy.arange(0.5, 27.5), 
            [reduce(lambda x, y: x + y, tup) for tup in itertools.product('012', repeat=3)])

#    return tbl.T


def makeMatrix(run, actions=False):
    titles = run['data'][0].keys()
    title_map = dict(zip(titles, range(len(titles))))
    all_values = []
    for r in run['data']:
        values = []
        for t in titles:
            values.append(r[t])
        all_values.append(values)
    title_map['rewards'] = len(title_map.keys())
    for (index, lst) in enumerate(all_values):
        lst.append(run['rewards'][index])
    if actions:
        title_map['actions'] = len(title_map.keys())
        for (index, lst) in enumerate(all_values):
            if run['actions'][index] == 'DSDV':
                lst.append(0)
            else:
                lst.append(1)
    return (title_map, numpy.array(all_values))


def makeFullMatrix(pickles, actions=False):
    data = [makeMatrix(run, actions)[1] for run in pickles]
    datashape = (len(data), data[0].shape[0], data[0].shape[1])
    fullData = numpy.zeros(datashape)
    for page in range(datashape[0]):
        fullData[page,:,:] = data[page]
    return (makeMatrix(pickles[0], actions)[0], fullData)


def plotAverageReward(titleMap, fullMatrix):
    pyplot.semilogy(fullMatrix.mean(0)[:, titleMap['rewards']])


def binVector(arr, centerBinEdges):
    binMat = numpy.zeros(arr.shape)
    for (i,s) in enumerate(sensorValues):
        medindices = numpy.nonzero(arr[numpy.nonzero(arr[:,i] >= centerBinEdges[i][0]), i] <= centerBinEdges[i][1])
        highindicies = numpy.nonzero(arr[:,i] > centerBinEdges[i][1]) 
        binMat[medindices, i] = 1
        binMat[highindicies, i] = 2
    return binMat


def binSensors(titleMap, fullMatrix, centerBinEdges=centerBinEdges_10s_lessperturbed):
    sensorMatrix = fullMatrix[:, :, [titleMap[x] for x in sensorValues]]
    sensorBinMatrix = numpy.zeros(sensorMatrix.shape)
    for page in range(fullMatrix.shape[0]):
        sensorBinMatrix[page, :, :] = binVector(sensorMatrix[page, :, :], centerBinEdges)
    return sensorBinMatrix


def actionsPerState(titleMap, fullMatrix):
    state_gen = itertools.product('012', repeat=3)
    actions = fullMatrix[:, :, titleMap['actions']]
    states = binSensors(titleMap, fullMatrix, centerBinEdges_10s_lessperturbed)
    states = states[:,1:,:]
    actions = actions[:,:-1]
    actions = actions.reshape((1,-1)).T
    states = states.reshape((-1,3))

    state_locations = []
    for state in state_gen:
        comparison_state = tuple(int(x) for x in state)
        state_locations.append((state, numpy.nonzero((states == comparison_state).all(1))))

    actions_per_state = [(state, actions[locs]) for (state, locs) in state_locations]
    p_DYMO = actions.sum() / len(actions)
    return (p_DYMO, actions_per_state)


def probabilityStateGivenAction(p_DYMO, actions_per_state):
    probability_sga = [(state, 1-((loc.sum()/loc.shape[0])/p_DYMO),
            (loc.sum()/loc.shape[0])/p_DYMO) for (state, loc) in actions_per_state]
    return probability_sga


def plotProbabilityStateGivenAction(titleMap, fullMatrix):
    nstates = 27
    p_DYMO, actions_per_state = actionsPerState(titleMap, fullMatrix)
    psga = probabilityStateGivenAction(p_DYMO, actions_per_state)
    table = numpy.array([(x[1], x[2]) for x in psga])
    pyplot.pcolor(table, cmap=pyplot.cm.gray)
    pyplot.title('Probability of state given action')
    pyplot.xlabel('Action')
    pyplot.xticks((0.5, 1.5), ('DSDV', 'DYMOFAU'))
    pyplot.ylim([0,nstates])
    pyplot.yticks(numpy.arange(0.5, 27.5), 
            [reduce(lambda x, y: x + y, tup) for tup in itertools.product('012', repeat=3)])
#            [tup for tup in itertools.product('lmh', repeat=3)])
    pyplot.ylabel('State (Level of load,speed,neighbors)')
    pyplot.draw()

    return table


def makeHighRunPlots(filename='./results_10s_lessperturbed_moreruns_rl_run', actions=True, rng=None):
    if rng is None:
        rng = range(1,6)
    pickles = loadPickles(filename, rng)
    titleMap, fullMatrix = makeFullMatrix(pickles, actions=actions)

    pyplot.figure()
    plotProbabilityStateGivenAction(titleMap, fullMatrix)

    pyplot.figure()
    plotPolicy(pickles)

    pyplot.figure()
    plotLoad(pickles[0])

    pyplot.figure()
    plotSpeed(pickles[0])

    pyplot.figure()
    plotNeighbors(pickles[0])


########
# Tests
########


def testBinning():
    fooTask = OmnetTask(OmnetEnvironment())
    print(fooTask.env.getSensors())
    print(fooTask.binValues(fooTask.env.getSensors()))
    print(fooTask.getObservation())


def testLinearization():
    fooTask = OmnetTask(OmnetEnvironment())
    for i in range(fooTask.env.numSensors):
        for j in range(fooTask.env.numSensors):
            for k in range(fooTask.env.numSensors):
                print((i,j,k), fooTask.linearizeIndex((i,j,k)))
