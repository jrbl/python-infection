#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Make .rst docs and upload to the CheeseShop.

After a strategy described by Will McKenzie
"""
import pandoc
import re
import os

import sys; sys.exit(127) # we don't want to register this 

pandoc.core.PANDOC_PATH = '/usr/bin/pandoc'

to_process = []
for f in os.listdir('.'):
    if re.match('.*\.md$', f):
        new_file = re.sub('(?P<base>.*)\.md$', 
                          lambda mo: mo.group('base')+'.rst',
                          f)
        to_process.append((f, new_file))

for old, new in to_process:
    doc = pandoc.Document()
    doc.markdown = open(old, 'rb').read()
    with open(new, 'wb') as rtsout:
        rtsout.write(doc.rst)

# TODO shouldn't this be subprocess or pipes or something?
os.system("python setup.py register sdist upload")

for old, new in to_process:
    os.remove(new)
