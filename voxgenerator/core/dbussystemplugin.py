#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbusabstractplugin import DbusAbstractPlugin

class DbusSystemPlugin(DbusAbstractPlugin):
    def __init__(self, name):
        DbusAbstractPlugin.__init__(self)
        self.__type__ = self.__bustypes__.System
        self.__name__ = name
        self.__finalizeinit__()
