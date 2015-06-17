#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import dbus.service
import dbus
from dbus.mainloop.glib import DBusGMainLoop
"""
http://www.documentroot.net/en/linux/python-dbus-tutorial
https://developer.pidgin.im/wiki/DbusHowto
"""

class DbusClient(dbus.service.Object):
    def __init__(self):
        self.__hyp__ = ""
        
        DBusGMainLoop(set_as_default=True)
        
        busName = dbus.service.BusName('org.freedesktop.Voxgenerator', bus = dbus.SessionBus())
        dbus.service.Object.__init__(self, busName, '/Voxgenerator')        

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_restart(self):
        print "Request to restart the client !"
    
    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_stop(self):
        print "Request to stop the client !"

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='s')
    def dbus_new_transcription(self, s):
        self.__hyp__ = s
    
    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='s')    
    def dbus_get_transcription(self):
        return self.__hyp__
