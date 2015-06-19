#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbusabstractplugin import DbusAbstractPlugin

class DbusSessionPlugin(DbusAbstractPlugin):
    def __init__(self, name):
        DbusAbstractPlugin.__init__(self)
        self.__name__ = name
        self.__type__ = self.__bustypes__.Session
        self.__finalizeinit__()
