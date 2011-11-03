#! /usr/bin/python
"""
Script to parse data output from Omnet++ and package it as JSON.

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

import json
import numpy
import sys
from pprint import pprint


def loadFile(filename='resultsBank.txt'):
    with open(filename) as fh:
        runs = json.load(fh)
    return runs

def makeMatrix(runs):
    titles = runs[0].keys()
    title_map = dict(zip(titles, range(len(titles))))
    all_values = []
    for r in runs:
        values = []
        for t in titles:
            values.append(r[t])
        all_values.append(values)
    return (title_map, numpy.array(all_values))

def getRanges(title_map, mat):
    five_number_summary = {}
    for title in title_map.keys():
        data = mat[:, title_map[title]].copy()
        data.sort()
        five_number_summary[title] = \
                (data[0],
                numpy.median(data[0:round(len(data)/3)]), 
                numpy.median(data),
                numpy.median(data[(round(len(data)/3) + 1):]), 
                data[-1])
    return five_number_summary


def getBins(five_number_summary, keys=None):
    if keys is None:
        keys = ['load', 'speed', 'neighbors']
    return tuple((five_number_summary[key][1], five_number_summary[key][3]) for key in keys)


#def printAllStats(five_number_summary):
#    print "%10s %15s %15s %15s %15s %15s"%('', 'min', 'tertile', 'median',
#            'tertile', 'max')
#    for stat in five_number_summary.keys():
#        print "%10s %15f %15f %15f %15f %15f"% (stat,
#            float(five_number_summary[stat][0]),
#            float(five_number_summary[stat][1]),
#            float(five_number_summary[stat][2]),
#            float(five_number_summary[stat][3]),
#            float(five_number_summary[stat][4]))
#   # print "%10s %15f %15f %15f (%15f %15f)"%(title, data.min(), data.mean(),
#   # data.max(), (((data.min() + data.mean()) / 2) + data.min()),
#   # (((data.max() + data.mean()) / 2) + data.mean()))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Needs a filename argument")
    filename = sys.argv[1]
    runs = loadFile(filename)
    tmap, mat = makeMatrix(runs)
    five_number_summaries = getRanges(tmap, mat)
#    printAllStats(
    pprint(five_number_summaries)
    pprint(getBins(five_number_summaries))
