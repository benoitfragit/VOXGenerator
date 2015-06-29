#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icontroller import IController
from view import View
from lxml import etree
import dbus, dbus.service, os, gobject
from dbus.mainloop.glib import DBusGMainLoop

class Controller(IController):
    def __init__(self):
        DBusGMainLoop(set_as_default=True)

        self.__servicestatus__  = False
        self.__description__    = None
        self.__pipelinestatus__ = False
        self.__plugins__        = {}
        self.__view__           = View(self, None)

        self.__initializecontroller__()

        self.__addnewconnection__("dbus_plugin_registration", "Action")

        self.__view__.title('Voxgenerator control')
        gobject.idle_add(self.__updateview__)
        self.__loop__ = gobject.MainLoop()
        self.__loop__.run()

    def __updateview__(self):
        try:
            self.__view__.update()
        except:
            self.__loop__.quit()

        return True

    def __initializecontroller__(self):
        self.__bus__ = dbus.SessionBus()

        """ initialize service and pipeline status """
        try:
            pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                            "/org/freedesktop/Voxgenerator/Pipeline")

            self.__pipelinestatus__ = pipe.dbus_pipeline_request_status()
            self.__servicestatus__ = True
        except:
            self.__servicestatus_ = False
            self.__pipelinestatus__  = False

    def __addnewconnection__(self, signal, name):
        self.__bus__.add_signal_receiver(self.__dbus_process_registration__,
                                         interface_keyword = 'org.freedesktop.Voxgenerator',
                                         signal_name=signal,
                                         path_keyword="/org/freedesktop/Voxgenerator/" + name,
                                         member_keyword=name)

    def __update_service__(self):
        if self.__servicestatus__ == False:
            try:
                pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                               "/org/freedesktop/Voxgenerator/Pipeline")
                pipe.dbus_pipeline_request_stop()
            except:
                print "Unable to stop the pipeline !"
        else:
            try:
                pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                               "/org/freedesktop/Voxgenerator/Pipeline")
                pipe.dbus_pipeline_request_stop()
            except:
                print "No need to stop the pipeline !"

            if self.__description__ is not None and os.path.isfile(self.__description__):
                os.system("run_voxgenerator " + self.__description__ + " &")

    def __update_plugins_list__(self):
        if self.__description__ is not None and os.path.isfile(self.__description__):
            pipeline_tree = etree.parse(self.__description__)
            root          = pipeline_tree.xpath("/pipelines")
            includes      = root[0].findall("include")

            self.__plugins__.clear()
            for f in includes:
                plugin_xml = f.get("file")

                if os.path.isfile(plugin_xml):
                    plugin_tree = etree.parse(plugin_xml)
                    plugins = plugin_tree.xpath("/plugins/plugin")

                    for plugin in plugins:
                        name = plugin.get("name")
                        if not self.__plugins__.has_key(name):
                            self.__plugins__[name] = False

    def __update_plugin_status__(self):
        for name in self.__plugins__:
            try:
                proxy = self.__bus__.get_object("org.freedesktop.Voxgenerator." + name,
                                            "/org/freedesktop/Voxgenerator/" + name)

                self.__plugins__[name] = True
                self.__addnewconnection__("dbus_plugin_registration", name)
            except:
                self.__plugins__[name] = False

        self.__view__.set_current_plugins(self.__plugins__)

    def __dbus_process_registration__(self, *a, **ka):
        print a, ka

    """
    API IController Implementation
    """
    def set_service_status(self, var):
        new_status = False
        if  var == 1 or var == True:
            new_status = True

        if self.__servicestatus__ != new_status:
            self.__servicestatus__ = new_status
            self.__update_service__()

    def set_pipeline_status(self, var):
        new_status = False
        if var == 1 or var == True:
            new_status = True

        if self.__pipelinestatus__ != new_status:
            self.__pipelinestatus__ = new_status
            print "pipeline playing " + str(new_status)

    def set_current_description(self, f):
        self.__description__ = f
        self.__update_plugins_list__()
        self.__update_plugin_status__()

    def get_current_description(self):
        return self.__description__

    def get_service_status(self):
        return self.__servicestatus__

    def get_pipeline_status(self):
        return self.__pipelinestatus__

    def get_current_plugins(self):
        return self.__plugins__
