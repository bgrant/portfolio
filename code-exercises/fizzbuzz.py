#!/usr/bin/env python
"""
Implementation of `fizzbuzz`, just to make sure I can :)

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

for x in xrange(1,101):
    if x % 3 == 0 and x % 5 == 0:
        print "FizzBuzz"
    elif x % 5 == 0:
        print "Buzz"
    elif x % 3 == 0:
        print "Fizz"
    else:
        print x
