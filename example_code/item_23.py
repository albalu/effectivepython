#!/usr/bin/env python3

# Copyright 2014 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Preamble to mimick book environment
import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 1
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)


# Example 2
from collections import defaultdict

def log_missing():
    print('Key added')
    return 0


# Example 3
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
# The following line is VERY poorly explained in the book; basically since
# the variable current is a normal python dictionary we can use it here as an
# input ot a collections.defaultdict class and the difference is that this new
# result dict provide a default value for missin keys using a function provided
# (here it is log_missing which is just lambda: 0)
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))


# Example 4
def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    # basically one point of using defaultdict with log_missin is NOT to deal
    # with checking whether keys that are in increments are also available
    # in result, we just set it to zero if it wasn't and just add the increment
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# Example 5
result, count = increment_with_report(current, increments)
assert count == 2
print(result)


# Example 6
class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# Example 7
counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method reference
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print("Example 7 with a class, # of added: {}".format(counter.added))
print(result)


# Example 8
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
counter()
assert callable(counter)


# Example 9
counter = BetterCountMissing()
result = defaultdict(counter, current)  # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print()
print("Example 9 which shows just by introducing __call__ method we can count "
      "the number of times defaultdict needed to set defaults by calling the "
      "class, this number is {} as expected \n __call__ method lets an object"
      " (e.g. a class) be called just like a function".format(counter.added))
print(result)
