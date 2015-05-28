#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from lxml import etree
from xlib_utils import XlibUtils
from plugin_generator import PlugineGenerator

class Selector:
        self.__display__ = XlibUtils()
        
        self.__priority__  = {}
        self.__plugins__   = {}
        self.__windows__   = {}
        self.__keywords__  = {}
        self.__areas__     = {}
        self.__activated__ = {}
        
        self.__current_model_id__ = -1
        
        self.__build__(xml)
    
    def __getvalidpluginnames__(self, include):
        for f in include:
            plugin_xml = f.get("file")
            plugin_generator = PluginGenerator(plugin_xml)

            if os.path.isfile(plugin_xml):
                plugin_tree = etree.parse(plugin_xml)
                plugins = plugin_tree.xpath("/plugins/plugin")
            
                for plugin in plugins:
                    if not self.__plugins__.has_key(plugin.get("name")):
                        self.__plugins__[plugin.get("name")] = plugin.get("id")
                        
    def __build__(self, xml):        
        if os.path.isfile(xml):
            pipeline_tree = etree.parse(xml)

            pipelines = pipeline_tree.xpath("/pipelines/pipeline") 
            includes  = pipeline_tree.xpath("/pipelines/include")
            
            self.__getvalidpluginnames__(includes)
            self.__parsepipelines__(pipelines)
            
    def __parsepipelines__(self, pipelines):
        for pipeline in pipelines:
            plugin   = pipeline.get("plugin")
            priority = pipeline.get("priority")
            default  = pipeline.get("default")
        
            if self.__plugins__.has_key(plugin):
                id = self.__plugins__[plugin]
                self.__priority__[id] = priority 

                self.__parseactivation__(id, pipeline)
                
                if default is "True":
                    self.__activated__[id] = True
                    self.__current_model_id__ = id
            else:
                print "Plugin " + plugin + " is not a valid plugin name, please give a valid one !\n"

    def __parseactivation__(self, id, pipeline):
        activations = pipeline.findall("activation")
        
        for active in activations:
            self.__activated__[id] = False
            
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
        for id in self.__windows__:
            if self.__windows__[id] == window:
                self.__activated__[id] = True
            else:
                self.__activated__[id] = False
        
        for id in self.__keywords__:
            if hyp == self.__keywords__[id]:
                self.__activated__[id] = True
            else:
                self.__activated__[id] = False
        
        for id in self.__areas__:
            area = self.__areas__[id]
            x, y = self.__display__.__compute_mouse_position__()
            
            if area[0] <= x and x <= area[1] and area[2] <= y and y <= area[3]:
                self.__activated__[id] = True
            else:
                self.__activated__[id] = False

        first_pass = True
        max_priority = 0
        max_id = 0
        
        for id in self.__activated__:
            priority = self.__priority__[id]
            
            if first_pass or max_priority < priority:
                if self.__activated__[id] == True:
                    first_pass   = False
                    max_priority = priority
                    max_id    = id
        
        if max_id is not -1:
            self.__current_model_id__ = max_id
            
            for id in self.__activated__:
                if id != max_id:
                    self.__activated__[id] = False

    def __getactivatedlm__(self, hyp):
        print self.__activated__
        self.__updateactivations__(hyp)
        
        for lm in self.__plugins__:
            if self.__plugins__[lm] == self.__current_model_id__:
                return lm
        
        return ""
