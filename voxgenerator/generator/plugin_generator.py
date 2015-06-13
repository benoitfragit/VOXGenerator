#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generator import Generator

import sys
from lxml import etree
import os.path

class PluginGenerator(Generator):
    def __init__(self, xml):    
        Generator.__init__(self)
        
        if os.path.isfile(xml):
            plugin_tree = etree.parse(xml)
            plugins = plugin_tree.xpath("/plugins/plugin")
            
            for plugin in plugins:
                self.__generate_plugin__(plugin, xml)
        else:
            print "XML file: " + xml + "  not valid !"
    
    def __generate_plugin__(self, plugin, xml):
        self.__generate_base__(plugin, xml)
        self.__generate_body__(plugin)
        self.__generate_close__()
    
    def __generate_base__(self, plugin, xml):
        self.__id__     = plugin.get("id")
        self.__name__   = plugin.get("name")
        self.__reload__ = plugin.get("reload")
        self.__ip__     = plugin.get("ip")
        self.__port__   = plugin.get("port")
        
        base = os.path.dirname(xml)
        plugin_str_name = base + "/" + self.__name__.lower() + ".py"
        
        self.__f__ = open(plugin_str_name, 'w')
        self.__put__("#!/usr/bin/env python\n# -*- coding: utf-8 -*-")
        self.__put__("")
        self.__put__("import os, logging    ")
        self.__put__("from voxgenerator import Plugin")
        
        self.__addPackageInclusion__(plugin)
        
        self.__put__("class " + self.__name__ + "(Plugin):")
        self.__right__()
        self.__put__("def __init__(self):")
        self.__right__()
        self.__put__("Plugin.__init__(self, '" + self.__ip__ + "', " + self.__port__ + ")")
        self.__put__("self.__id__ = " + self.__id__)
        self.__put__("self.__name__ = '" + self.__name__ + "'\n")  
        self.__put__("self.__logger__ = logging.getLogger('voxgenerator." +  self.__name__ +  "')")

    def __generate_body__(self, plugin):
        commands = plugin.findall("command")          
        self.__addfunctionlookup__(commands)
        self.__addcommandlookup__(commands)
        self.__put__("self.__build__('" + self.__name__ + "'" + ", " + self.__reload__ + ")")
        self.__put__("self.__receive__()")
        self.__left__()
        self.__addcommandfunction__(commands)
        self.__left__()
    
    def __addPackageInclusion__(self, plugin):
        packages = plugin.findall("package")
        
        for package in packages:
            name = package.get("name")
            module = package.get("module")
            
            if name is not None and module is not None:
                self.__put__("from " + name + " import " + module)
            else:
                if name is not None and module is None:
                    self.__put__("import " + name)
            
    def __addfunctionlookup__(self, commands):
        id = 0        
        for cmd in commands:
            name    = cmd.get("name")
            self.__put__("self.__function__[" + str(id) + "] = self." + name)
            id += 1
            
        self.__put__("")

    def __addcommandlookup__(self, commands):
        id = 0
        for cmd in commands:
            trans   = cmd.get("transcription")
            self.__put__("self.__command__[" + str(id) + "] = '" + trans + "'")
            id += 1

        self.__put__("")

    def __addcommandfunction__(self, commands):
        id = 0
        for cmd in commands:
            id += 1
            self.__put__("")
            name    = cmd.get("name")
            type    = cmd.get("type")
            self.__put__("def " + name + "(self):")
            self.__right__()
            exe = cmd.get("exec")
            if exe is not None:
                if type == "system":
                    self.__put__("os.system('" + exe +"')")
                else:
                    self.__put__(exe)
            else:
                self.__put__("raise NotImplementedError('subclasses must override " + name + "()!')")
            
            self.__left__()
        
if __name__ == '__main__':
    plugin_generator = PluginGenerator(sys.argv[1])
