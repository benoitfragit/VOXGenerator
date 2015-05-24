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
            plugins = plugin_tree.xpath("/Plugins/Plugin")
            
            for plugin in plugins:
                self.__generate_plugin__(plugin)
        else:
            print "XML file: " + xml + "  not valid !"
    
    def __generate_plugin__(self, plugin):
        self.__generate_base__(plugin)
        self.__generate_body__(plugin)
        self.__generate_close__()
    
    def __generate_base__(self, plugin):
        self.__id__     = plugin.get("id")
        self.__name__   = plugin.get("name")
        self.__reload__ = plugin.get("reload")
        plugin_str_name = self.__name__ + ".py"
        
        self.__f__ = open(plugin_str_name, 'w')
        self.__put__("#!/usr/bin/env python\n# -*- coding: utf-8 -*-")
        self.__put__("")
        self.__put__("import os")
        self.__put__("from plugin import Plugin")
        
        self.__put__("class " + self.__name__ + "(Plugin):")
        self.__right__()
        self.__put__("def __init__(self):")
        self.__right__()
        self.__put__("Plugin.__init__(self)")
        self.__put__("self.__id__ = " + self.__id__)
        self.__put__("self.__name__ = '" + self.__name__ + "'\n")  

    def __generate_body__(self, plugin):
        commands = plugin.findall("Command")            
        self.__addfunctionlookup__(commands)
        self.__addcommandlookup__(commands)
        self.__put__("self.__build__('" + self.__name__ + "'" + ", " + self.__reload__ + ")")
        self.__left__()
        self.__addcommandfunction__(commands)
        self.__left__()
    
    def __addfunctionlookup__(self, commands):        
        for cmd in commands:
            id      = cmd.get("id")
            name    = cmd.get("name")
            self.__put__("self.__function__[" + id + "] = self." + name)
            
        self.__put__("")

    def __addcommandlookup__(self, commands):
        for cmd in commands:
            id      = cmd.get("id")
            trans   = cmd.get("transcription")
            self.__put__("self.__command__[" + id + "] = '" + trans + "'")

        self.__put__("")

    def __addcommandfunction__(self, commands):
        for cmd in commands:
            self.__put__("")
            id      = cmd.get("id")
            name    = cmd.get("name")
            type    = cmd.get("type")
            self.__put__("def " + name + "(self):")
            self.__right__()
            if type == "system":
                exe = cmd.get("exec")
                self.__put__("os.system('" + exe +"')")
            else:
                self.__put__("print 'not yet implemented'")
            
            self.__left__()
    
if __name__ == '__main__':
    plugin_generator = PluginGenerator(sys.argv[1])
