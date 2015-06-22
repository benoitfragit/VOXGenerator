#!/usr/bin/env python
# -*- coding: utf-8 -*-

from voxgenerator.pipeline import Pipeline

import os, sys

if __name__ == '__main__':
    if len(sys.argv) >= 2 and os.path.isfile(sys.argv[1]):
        p = Pipeline(sys.argv[1])
        p.__run__()
