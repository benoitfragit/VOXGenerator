from voxgenerator import Checksum
from voxgenerator import PluginGenerator
from voxgenerator import ModelGenerator

import sys

if __name__ == '__main__':
    checker = Checksum()
    if checker.__haschanged__(sys.argv[1]):
        plugin_generator = PluginGenerator(sys.argv[1])
        model_generator  = ModelGenerator(sys.argv[1], sys.argv[2])
