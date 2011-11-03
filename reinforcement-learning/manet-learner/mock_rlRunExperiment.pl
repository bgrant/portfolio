#! /usr/bin/python
"""
A mock in place of the real perl script which runs an experiment in
Omnet++ and prints similar looking data to stdout.

:author: Robert David Grant <robert.david.grant@gmail.com>
:author: Agoston Petz

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

