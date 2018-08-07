# -*- coding: utf-8 -*-
# Copyright (c) 2018 Hoël Iris

# MIT License

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='stripe-hooks',
    version=0.1,
    author='Hoël Iris',
    author_email='hoel.iris@gmail.com',
    url='https://github.com/tolteck/stripe-hooks',
    description=('A low-configuration service for sending notifications and'
                 'receipts based on Stripe webhooks.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['stripe_hooks'],
    entry_points={'console_scripts':
                  ['stripe-hooks=stripe_hooks.__main__:start']},
    install_requires=[
        'Flask >= 1.0.2',
        'stripe >= 2.4.0',
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ),
)
