#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbussessionplugin import DbusSessionPlugin

"""
@Todo
add a signal receiver fonc to connect the pluin to the
signal emitted by the pipeline
"""

class DbusPlugin(DbusSessionPlugin):
    def __init__(self, name):
        DbusSessionPlugin.__init__(self, name)
        self.__bus__.add_signal_receiver(self.__dbus_process_hyp__,
                                        interface_keyword = 'org.freedesktop.Voxgenerator',
                                        member_keyword = 'Pipeline',
                                        path_keyword = self.__dbus_path__ + '/Voxgenerator/Pipeline')

    def __dbus_process_hyp__(self, *a, **ka):
        if self.__is_command_valid__(*a):
            self.__process__(a[1])

    def __process__(self, hyp):
        raise NotImplementedError('Subclasses must override !')

    def __is_command_valid__(self, *a):
        if len(a) > 1 and a[0] == self.__name__:
            self.__logger__.info("Plugin: " + self.__name__ + " will proceed command: " + a[1])
            return True
        else:
            return False
