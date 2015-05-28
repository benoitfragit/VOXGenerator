#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from lxml import etree
from xlib_utils import XlibUtils
from plugin_generator import PluginGenerator
from model_generator import ModelGenerator
from checksum import Checksum

class Selector:
    def __init__(self, xml):
        self.__display__ = XlibUtils()
        
        self.__priority__  = {}
        self.__plugins__   = {}
        self.__windows__   = {}
        self.__keywords__  = {}
        self.__areas__     = {}
        self.__current_model_id__ = -1
        self.__lmctl__ = ""
        self.__default__ = ""
        self.__build__(xml)

    def __getvalidpluginnames__(self, include):
        for f in include:
            plugin_xml = f.get("file")
                        
            checker = Checksum()
            if checker.__haschanged__(plugin_xml):
                plugin_generator = PluginGenerator(plugin_xml)
                model_generator  = ModelGenerator(plugin_xml, self.__lmctl__)

            if os.path.isfile(plugin_xml):
                plugin_tree = etree.parse(plugin_xml)
                plugins = plugin_tree.xpath("/plugins/plugin")
            
                for plugin in plugins:
                    if not self.__plugins__.has_key(plugin.get("name")):
                        self.__plugins__[plugin.get("name")] = plugin.get("id")
                        
    def __build__(self, xml):
        if os.path.isfile(xml):
            pipeline_tree = etree.parse(xml)

            root      = pipeline_tree.xpath("/pipelines")
            pipelines = root[0].findall("pipeline") 
            includes  = root[0].findall("include")
            lmctl     = root[0].find("lmctl")
            self.__lmctl__ = lmctl.get("file")
            
            self.__getvalidpluginnames__(includes)
            self.__parsepipelines__(pipelines)
            
    def __parsepipelines__(self, pipelines):
        for pipeline in pipelines:
            plugin   = pipeline.get("plugin")
            priority = pipeline.get("priority")
            default  = pipeline.get("default")
        
            if self.__plugins__.has_key(plugin):
                id = self.__plugins__[plugin]
                self.__priority__[priority] = id 

                self.__parseactivation__(id, pipeline)
                
                if default == "True":
                    self.__current_model_id__ = id
                    self.__default__ = plugin
            else:
                print "Plugin " + plugin + " is not a valid plugin name, please give a valid one !\n"

    def __parseactivation__(self, id, pipeline):
        activations = pipeline.findall("activation")
        
        for active in activations:            
            window = active.get("window") 
            if window is not None:
                self.__windows__[id] = window;
            
            if active.get("mouse") is "True":
                x = active.find("x")
                y = active.find("y")
                self.__areas__[id] = [int(x.get("start")), int(x.get("end")), int(y.get("start")), int(y.get("end"))]
            
            keyword = active.get("keyword")
            if keyword is not None:
                self.__keywords__[id] = keyword

    def __updateactivations__(self, hyp):
        window = self.__display__.__compute_active_window__() 
        x, y = self.__display__.__compute_mouse_position__()
        
        sorted_priority = sorted(self.__priority__, key=self.__priority__.__getitem__) 
        
        for id in sorted_priority:
            if id in self.__windows__ and self.__windows__[id] == window:
                self.__current_model_id__ = id
                break
        
            if id in self.__keywords__ and hyp == self.__keywords__[id]:
                self.__current_model_id__ = id
                break

            if id in self.__areas__:
                area = self.__areas__[id]
            
                if area[0] <= x and x <= area[1] and area[2] <= y and y <= area[3]:
                    self.__current_model_id__ = id
                    break

    def __getactivatedlm__(self, hyp):
        self.__updateactivations__(hyp)
        
        for lm in self.__plugins__:
            if self.__plugins__[lm] == self.__current_model_id__:
                return lm
        
        return self.__default__

    def __getdefault__(self):
        return self.__default__
