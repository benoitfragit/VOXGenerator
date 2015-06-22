#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import dbus.service
import dbus, logging
from dbus.mainloop.glib import DBusGMainLoop

class DbusAbstractPlugin(dbus.service.Object):
    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        logging.basicConfig(level=logging.DEBUG)

        self.__dbus_path__      = '/Voxgenerator'
        self.__logger__         = logging.getLogger('org.freedesktop.Voxgenerator')
        self.__bustypes__       = self.enumbus("Invalid", "Session", "System")
        self.__type__           = self.__bustypes__.Invalid
        self.__name__           = ''

        self.__availablebus__ = {self.__bustypes__.Session : dbus.SessionBus(),
                                 self.__bustypes__.System  : dbus.SystemBus()}

        self.__loop__ = gobject.MainLoop()

    def __finalizeinit__(self):
        if self.__availablebus__.has_key(self.__type__):
            self.__bus__ = self.__availablebus__[self.__type__]
            busName = dbus.service.BusName('org.freedesktop.Voxgenerator', self.__bus__)
        else:
            busName = dbus.service.BusName('org.freedesktop.Voxgenerator', dbus.SessionBus)
            self.__bus__ = dbus.dbusSession

        dbus.service.Object.__init__(self, busName, self.__dbus_path__ + '/' + self.__name__)
        self.dbus_plugin_registration()
        self.__logger__.info("dbus: " + self.__name__ + " has been inititialized!")

    def enumbus(self, *args):
        enum = dict(zip(args, range(len(args))))
        return type('Enum', (), enum)

    def __run__(self):
        self.__logger__.info("dbus: " + self.__name__ + " has started!")
        self.__loop__.run()

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_plugin_registration(self):
        self.__logger__.info("Registering: " + self.__dbus_path__ + "/" + self.__name__)
