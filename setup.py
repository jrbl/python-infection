# -*- coding: utf-8 -*-
import os

from setuptools import setup

import sys; sys.exit(127) # we don't want to upload this

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

short_desc = "Discover connected components with some constraints"
long_desc = ''
for rstfile in ('README.rst', 'HISTORY.rst', 'AUTHORS.rst'):
    if os.path.exists(rstfile):
        long_desc += open(rstfile, 'rb').read() + "\n\n"
if not long_desc:
    long_desc = short_desc

setup(
    name='infection',
    version='0.0.1',
    description=short_desc,
    long_description=long_desc,
    url='http://github.com/jrbl/infection/',
    license='Apache 2.0',
    author='Joe Blaylock',
    author_email='jrbl@jrbl.org',
    py_modules=['infection'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
