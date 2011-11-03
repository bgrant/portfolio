"""
Implementation of concurrent producer and consumer threads using Queue
module.

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
from __future__ import with_statement
import threading
import Queue

class Producer(threading.Thread):
    '''Producer thread'''
    def __init__(self, q, run_length=1000):
        self.q = q
        self.run_length = run_length
        threading.Thread.__init__(self)

    def run(self):
        for _ in range(self.run_length):
            self.q.put('.', block=True)
            print self.q.qsize()


class Consumer(threading.Thread):
    '''Consumer thread'''
    def __init__(self, q, run_length=1000):
        self.q = q
        self.run_length = run_length
        threading.Thread.__init__(self)

    def run(self):
        for _ in range(self.run_length):
            item = self.q.get(block=True)
            print self.q.qsize()


def main():
    '''Run the Producer and Consumer'''
    run_length=1000000
    q = Queue.Queue(50)
    p = Producer(q, run_length)
    c = Consumer(q, run_length)

    p.start()
    c.start()

    p.join()
    c.join()

    print "Threads completed"
