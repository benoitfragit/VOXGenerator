#!/usr/bin/env python

from voxgenerator import Pipeline

import sys

if __name__ == '__main__':    
    p = Pipeline(sys.argv[1])
    p.__play__()
