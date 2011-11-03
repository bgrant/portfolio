"""
Playing with basic bayesian computations.

:author: Robert David Grant <robert.david.grant@gmail.com>

:copyright: 
    Copyright 2011 Robert David Grant

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
from numpy import linspace, array, argmax
from pylab import plot, xlabel, ylabel, title

def coin_flip():
    if random.random() < (1.0/3.0):
        return 1
    else:
        return 0

def binomial(H, data):
    ntosses = len(data)
    nheads = sum(data)
    return (H**nheads) * (1-H)**(ntosses-nheads)

def uniform(H):
    if (0 <= H <= 1):
        return 1
    else:
        return 0

def posterior(data, H):
    likelihood = binomial(H, data)
    prior = uniform(H)
    return likelihood * prior

def experiment(trials=10):
    data = [coin_flip() for x in range(trials)]
    hypotheses = linspace(0,1,1001)
    posterior_dist = array([posterior(data, H) for H in hypotheses])
    print "Best estimate: %f" % (hypotheses[posterior_dist.argmax()],)
    normalization_factor = posterior_dist.sum()
    normalized_posterior = posterior_dist / normalization_factor
    return (normalized_posterior, hypotheses)

def plot_posterior(posterior_dist, hypotheses):
    plot(hypotheses, posterior_dist)
    xlabel("Bias-weighting for heads H")
    ylabel("prob(H|data,I)")

def main()
    plot_posterior(*experiment())
