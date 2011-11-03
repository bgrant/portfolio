"""
Playing with sorting algorithms in python.

Done in 2007 while preparing for interviews.

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

# Mergesort
def mergesort(lst):
    if len(lst) <= 1:
        return lst
    left = mergesort(lst[:len(lst)/2])
    right = mergesort(lst[len(lst)/2:])
    return merge(left, right)

def merge(left, right):
    merged = []
    lpos = rpos = 0
    while lpos < len(left) and rpos < len(right):
        if left[lpos] < right[rpos]:
            merged.append(left[lpos])
            lpos += 1
        else:
            merged.append(right[rpos])
            rpos += 1
    if lpos != len(left):
        merged.extend(left[lpos:])
    elif rpos != len(right):
        merged.extend(right[rpos:])
    return merged

# Quicksort
def quicksort(lst):
    if len(lst) <= 1:
        return lst
    less = []
    greater = []
    #ppos = random.randint(0, len(lst)-1) # pivot
    ppos = len(lst)/2
    for x in lst[:ppos]+lst[ppos+1:]:
        if x < lst[ppos]:
            less.append(x)
        else:
            greater.append(x)
    return quicksort(less) + [lst[ppos]] + quicksort(greater)

# Bubblesort
def bubblesort(lst):
    sorted = False
    while sorted is False:
        sorted = True
        for i,x in enumerate(lst[:-1]):
            if lst[i] > lst[i+1]:
                lst[i],lst[i+1] = lst[i+1],lst[i]
                sorted = False
    return lst
