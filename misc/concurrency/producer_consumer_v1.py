"""
Implementation of concurrent producer and consumer threads using a stack
synchronized with locks.

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

class Stack:
    '''Synchronized stack'''
    def __init__(self, max=10):
        self.__data = []
        self.__max = max
        self.__lock = threading.Lock()
        self.__produce = threading.Condition(self.__lock)

    def __repr__(self):
        self.__lock.acquire()
        stack = self.__data.__repr__()
        self.__lock.release()
        return stack

    def push(self, item):
        self.__lock.acquire()
        assert(len(self.__data) <= self.__max)
        assert(len(self.__data) >=0)
        while len(self.__data) == self.__max:
            self.__produce.wait()
        assert(len(self.__data) < self.__max)
        assert(len(self.__data) >= 0)
        self.__data.append(item)
        print len(self.__data)
        self.__produce.notify()
        self.__lock.release()

    def pop(self):
        self.__lock.acquire()
        assert(len(self.__data) <= self.__max)
        assert(len(self.__data) >=0)
        while len(self.__data) == 0:
            self.__produce.wait()
        assert(len(self.__data) <= self.__max)
        assert(len(self.__data) > 0)
        item = self.__data.pop()
        print len(self.__data)
        self.__produce.notify()
        self.__lock.release()
        return item


class Producer(threading.Thread):
    '''Producer thread'''
    def __init__(self, stack, run_length=1000):
        self.stack = stack
        self.run_length = run_length
        threading.Thread.__init__(self)

    def run(self):
        n = 0
        while(n < self.run_length):
            self.stack.push('.')
            n += 1


class Consumer(threading.Thread):
    '''Consumer thread'''
    def __init__(self, stack, run_length=1000):
        self.stack = stack
        self.run_length = run_length
        threading.Thread.__init__(self)

    def run(self):
        n = 0
        while(n < self.run_length):
            item = self.stack.pop()
            n += 1


def main():
    '''Run the Producer and Consumer'''
    run_length=1000000
    s = Stack()
    p = Producer(s, run_length)
    c = Consumer(s, run_length)

    p.start()
    c.start()

    p.join()
    c.join()

    print "Threads completed"
