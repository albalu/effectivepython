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
class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


# Example 2
data = LazyDB()
print('Before:', data.__dict__)
print('foo:   ', data.foo)
print('After: ', data.__dict__)


# Example 3
class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)


# Example 4
class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)


# Example 5
try:
    class MissingPropertyDB(object):
        def __getattr__(self, name):
            if name == 'bad_name':
                raise AttributeError('%s is missing' % name)
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

    data = MissingPropertyDB()
    data.foo  # Test this works
    data.bad_name
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
data = LoggingLazyDB()
print()
print("Exaple 6: showing that hasattr also calls on __getattr__ but only once")
print('Before:     ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))
print('After:      ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))


# Example 7
data = ValidatingDB()
print()
print("Example 7: note that ValidatingDB calls on __getattribute__ each time")
print('foo exists: ', hasattr(data, 'foo'))
print('foo exists: ', hasattr(data, 'foo'))


# Example 8
class SavingDB(object):
    def __setattr__(self, name, value):
        # Save some data to the DB log
        super().__setattr__(name, value)


# Example 9
class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)

data = LoggingSavingDB()
print()
print("Example 9: everytime we assign a value to foo, __setattr__ is called!")
print('Before: ', data.__dict__)
data.foo = 5
print('After:  ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)


# Example 10
print()
print("Example 10: recursion depth exceeds as everytime __getattribute__"
      "accesses self._data, __getattribute__ is called again!")
class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]


# Example 11
try:
    data = BrokenDictionaryDB({'foo': 3})
    data.foo
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
print()
print("Example 12: this time we access the data from the instance "
      "attribute dictionary to avoid recursion")


class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryDB({'foo': 3})
print(data.foo)
