#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from command_selector import FuzzySelector
from agent import PluginAgent

class Plugin(PluginAgent):
    def __init__(self):
        PluginAgent.__init__(self)
        self.__selector__ = FuzzySelector()
        self.__function__ = {}
        self.__command__  = {}

    def __build__(self, name, rebuild):
        self.__selector__.__build__(name, self.__command__, rebuild)
