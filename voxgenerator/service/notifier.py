#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus

class Notifier:
    def __init__(self):
        self.__item__      = "org.freedesktop.Notifications"
        self.__path__      = "/org/freedesktop/Notifications"
        self.__interface__ = "org.freedesktop.Notifications"
        self.__app_name__  = "Voxgenerator"
        self.__id__        = 0

        self.__bus__       = dbus.SessionBus()

    def __notify__(self, icon, title, text, timeout):
        actions_list       = ''
        hint               = ''

        notif              = self.__bus__.get_object(self.__item__, self.__path__)
        notify             = dbus.Interface(notif, self.__interface__)
        notify.Notify(self.__app_name__, self.__id__, icon, title, text, actions_list, hint, timeout)

if __name__ == '__main__':
    Notifier().__notify__("", "Test", "test", 2000)
