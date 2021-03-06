#!/usr/bin/env python

"""
Software for controlling a Player server, running on Gumstix hardware,
controlling an iRobot Create.

It's main features are a Node class and a function do_random_direction
that makes an iRobot Create perform the Random Direction mobility model.
The Node class provides (in the author's view) an easier,
object-oriented interface for controlling the iRobot Create from python.  

This script is intended to be run from a python interactive shell, and
thus its 'main' function currently does nothing.  If you run this script
from the python interactive shell it is easy to instantiate a Node
object and give commands to the Create in the form of Node methods.  An
example function using the Node class is the do_random_direction
function.

:author: Robert Grant <bgrant@mail.utexas.edu>

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

import math
import random
import time
from math import pi
from playerc import *

class Node:
    'Abstraction of an iRobot Create mobile node'

    def __init__(self, client_address):
        'Create a client object and subscribe to some sensor proxies'

        # Create a client object
        self.client = playerc_client(None, client_address, 6665)

        # Connect it
        if self.client.connect() != 0:
          raise playerc_error_str()

        # Create a proxy for position2d:0
        self.pos2d = playerc_position2d(self.client, 0)
        if self.pos2d.subscribe(PLAYERC_OPEN_MODE) != 0:
          raise playerc_error_str()

        # Create a proxy for the bumper
        self.bumper = playerc_bumper(self.client, 0)
        if self.bumper.subscribe(PLAYERC_OPEN_MODE) != 0:
          raise playerc_error_str()

    def disconnect(self):
        'Close down the connections'
        self.bumper.unsubscribe()
        self.pos2d.unsubscribe()
        self.client.disconnect()

    def velocity(self, speed, radians_per_second):
        'Set the linear and angular velocities'
        self.pos2d.set_cmd_vel(speed, 0.0, radians_per_second, 1)

    def stop(self):
        'Set the velocity parameters to stop the node\'s motion'
        self.velocity(0.0, 0.0)

    def turn_speed(self, radians_per_second):
        'Set the angular velocity of the node in radians/s.  Very inaccurate.'
        self.velocity(0.0, radians_per_second)

    def turn_angle(self, radians):
        '''Attempt to turn a specific anglular amount by turning at particular
        angular velocity for a certain amount of time.  Must be calibrated with
        internal angle_calibration_factor.'''
        angle_calibration_factor = 0.52

        self.read()
        original_angle = self.get_angle()
        speed = pi/8

        if radians >= 0:
            self.turn_speed(pi/8)
        else:
            self.turn_speed(-pi/8)

        time.sleep(abs(radians/speed * angle_calibration_factor))
        self.stop()

    def forward(self, speed):
        'Set a node\'s linear velocity only'
        self.velocity(speed, 0.0)

    def read(self):
        '''Command to pull sensor data from the node.  Must be polled constantly
        or node message queue will overflow and data will be lost.'''
        self.client.read()

    def get_bumper(self):
        'Get the last read() bumper data.'
        #self.bumper.bumpers returns a list of 32 values, but it looks like
        #only the first two are set
        return (self.bumper.bumpers[0], self.bumper.bumpers[1])

    def get_position(self):
        'Get the last read() position data (x pos, y pos, angular pos).'
        return (self.pos2d.px, self.pos2d.py, self.pos2d.pa)

    def get_angle(self):
        'Get the last read() angular position data.'
        return self.pos2d.pa

def random_angle():
    'Pick a turn angle in union([-pi/2,-pi],[pi/2, pi])'

    angle = random.uniform(-pi/2, pi/2)
    if angle < 0:
        angle -= pi/2
    else:
        angle += pi/2

    return angle

def do_random_direction(ip_addr):
    'Have a node perform the Random Direction mobility model'

    node = Node(ip_addr)
    node_speed = 0.2 # m/s

    try:
        # go forward until node runs into something
        node.forward(node_speed)

        while 1:
            node.read()
            print node.get_bumper()

            if sum(node.get_bumper()) != 0:
                # if the node runs into something, back up a bit to get
                # untangled
                node.forward(-node_speed)
                time.sleep(1)
                node.stop()

                # clear the next few sensor samples or else the node will think
                # it's still bumping against something and 
                for x in range(5):
                    node.read()

                print node.get_bumper()

                # pick a new angle and go again
                node.turn_angle(random_angle())
                node.forward(node_speed)
    finally:
        # it seems not to hurt anything if we don't disconnect at the end, but
        # we should clean up anyway
        node.disconnect() 

def main():
    '''Nothing in main() right now.  I\'ve been calling the functions from the
    interactive shell'''
    pass

if __name__ == '__main__':
    main()
