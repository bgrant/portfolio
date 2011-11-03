"""
Dining philosophers simulation.

:author: Robert David Grant <robert.david.grant@gmail.com>

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

import threading
from time import sleep
from random import uniform


class Philosopher(threading.Thread):
    '''Dining Philosopher'''
    def __init__(self, table, number, nIter=-1):
        self.number = number
        self.lChop = None
        self.rChop = None
        self.nIter = nIter
        threading.Thread.__init__(self)

    def think(self, min=0, max=1):
        print "Philosopher " + str(self.number) + " thinking"
        sleep(uniform(min,max))

    def eat(self, min=0, max=1):
        print "Philosopher " + str(self.number) + " eating"
        sleep(uniform(min,max))

    def sitAndEat(self):
        self.lChop.pickup()
        self.rChop.pickup()
        self.eat()
        self.rChop.putdown()
        self.lChop.putdown()

    def run(self):
        i = 0
        while(i != self.nIter):
            self.sitAndEat()
            self.think()
            i += 1


class Chopstick():
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def pickup(self):
        self.lock.acquire()

    def putdown(self):
        self.lock.release()


class Table():
    def __init__(self, n):
        self.pList = []
        self.cList = []
        for i in range(n):
            self.pList.append(Philosopher(self, i))
            self.cList.append(Chopstick())
        for i,p in enumerate(self.pList):
            p.lChop = self.cList[(i-1)%5]
            p.rChop = self.cList[i]

    def run(self):
        for i,p in enumerate(self.pList):
            print "Running philosopher " + str(i)
            p.start()
        for p in self.pList:
            p.join()


def main():
    nPhilosophers = 5
    table = Table(nPhilosophers)
    table.run()
