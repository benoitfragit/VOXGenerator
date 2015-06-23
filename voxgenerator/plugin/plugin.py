#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging
from command_selector import FuzzySelector
from voxgenerator.core import DbusPlugin

class Plugin(DbusPlugin):
    def __init__(self, name):
        DbusPlugin.__init__(self, name)

        self.__selector__ = FuzzySelector()
        self.__function__ = {}
        self.__command__  = {}

    def __build__(self, rebuild):
        self.__selector__.__build__(self.__name__.lower(), self.__command__, rebuild)

    def __process__(self, hyp):
        idx = self.__selector__.__query__(hyp)
        self.__logger__.info('command: ' + self.__command__[idx])

        if self.__function__.has_key(idx):
            try:
                self.__function__[idx]()
            except:
                self.__logger__.warning("you should overwrite method" + self.__command__[idx])

