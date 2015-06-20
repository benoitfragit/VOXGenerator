#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbussessionplugin import DbusSessionPlugin

class DbusPlugin(DbusSessionPlugin):
    def __init__(self, name):
        DbusSessionPlugin.__init__(self, name)
        self.__bus__.add_signal_receiver(__dbus_process_hyp__, )
    
    def __dbus_process_hyp__(self, lm, hyp):
        raise NotImplementedError('subclasses must override __dbus_process_hyp_()!')
