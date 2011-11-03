#! /usr/bin/python

import json
from numpy import array
from numpy.random import randint, random

centerBinEdges = ((12.194000, 273.562000),
                 (2.825204, 8.191208),
                 (4.000000, 10.000000))
sensorValues = ('load', 'speed', 'neighbors', 'throughput', 'latency')
startValues = array([2*(centerBinEdges[0][1] - centerBinEdges[0][0])*random() + array(centerBinEdges[0]).mean(), 
                    2*(centerBinEdges[1][1] - centerBinEdges[1][0])*random() + array(centerBinEdges[1]).mean(), 
                    randint(0, 2*centerBinEdges[2][1]), 
                    randint(0,11),
                    .000001*random() + 0.000010])

if random() < 0.1:
    print '{Garbage!'
else:
    print json.dumps(dict(zip(sensorValues, startValues)))

