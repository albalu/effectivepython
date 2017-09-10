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


# Example 3
from tempfile import TemporaryDirectory
from unittest import TestCase


class MyTest(TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()
        print()
        print('test setUp...')
        print('Use setUp and teardown only when you need to have some'
              'special environment (e.g. a temp folder like follows) setup!')
        print('temporary directory: {}'.format(self.test_dir))

    def tearDown(self):
        self.test_dir.cleanup()
        print()
        print('test tearDown...')

    # Test methods follow
    def test(self):
        print()
        print('the actual test here...')

    # note how naming the functions matter!
    def some_other_test(self):
        print()
        print('this test does not run!')

    def test_other(self):
        print()
        print('test number 2 ...')