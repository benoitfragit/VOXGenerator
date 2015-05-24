#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generator import Generator
import sys
from lxml import etree
import os.path

class PipelineGenerator(Generator):
    def __init__(self, xml):
        Generator.__init__(self)
        
        self.__plugins__ = {}
        
        if os.path.isfile(xml):
            pipeline_tree = etree.parse(xml)

            pipelines = pipeline_tree.xpath("/Pipelines/Pipeline") 
            includes  = pipeline_tree.xpath("/Pipelines/Include")
            
            self.__get_valid_plugin_names__(includes)
            
            for pipeline in pipelines:
                self.__generate_pipeline__(pipeline)
        else:
            print "XML file: " + xml + "  not valid !\n"
    
    def __get_valid_plugin_names__(self, include):
        for f in include:
            plugin_xml = f.get("file")

            if os.path.isfile(plugin_xml):
                plugin_tree = etree.parse(plugin_xml)
                plugins = plugin_tree.xpath("/Plugins/Plugin")
            
                for plugin in plugins:
                    if not self.__plugins__.has_key(plugin.get("name")):
                        self.__plugins__[plugin.get("name")] = plugin.get("id")
    
    def __generate_pipeline__(self, pipeline):
        plugin = pipeline.get("plugin")
        
        if self.__plugins__.has_key(plugin):
            self.__generate_base__(pipeline)
        else:
            print "Plugin " + plugin + " is not a valid plugin name, please give a valid one !\n"

    def __generate_pipeline__(self, pipeline):
        if self.__generate_base__(pipeline):
            self.__generate_body__(pipeline)
            self.__generate_close__()

    def __generate_close__(self):
        self.__put__("")
        self.__put__("if __name__ == '__main__':")
        self.__right__()
        self.__put__("p = " + self.__name__ + "()")
        self.__put__("p.__play__()")
        self.__left__() 
        self.__f__.close()       
        
    def __generate_base__(self, pipeline):
        plugin = pipeline.get("plugin")
        self.__id__  = self.__plugins__[plugin]
        self.__hmm__ = pipeline.get("hmm")
        self.__dic__ = pipeline.get("dic")
        self.__lm__  = "lm/" + plugin + ".lm.dmp" 
        self.__name__ = plugin + "VoicePipeline"

        if not os.path.isfile(self.__dic__):
            print 'Sphinx dictionnary ' + self.__dic__ + " does not exist !"
            return False
    
        if not os.path.isdir(self.__hmm__):
            print 'Sphinx hmm ' + self.__hmm__ + 'does not exist !'
            return False
    
        if not os.path.isfile(self.__lm__):
            print 'Sphinx lm file ' + self.__lm__ + 'does not exist !'
            return False

        pipeline_str_name = plugin + "_pipeline.py"
        self.__f__ = open(pipeline_str_name, 'w')
        self.__put__("#!/usr/bin/env python\n# -*- coding: utf-8 -*-")
        self.__put__("")
        self.__put__("import os")
        self.__put__("from pipeline import Pipeline")
        self.__put__("from xlib_utils import XlibUtils")
        self.__put__("")
        self.__put__("class " + self.__name__ + "(Pipeline):")
        self.__right__()
        self.__put__("def __init__(self):")
        self.__right__()
        self.__put__("Pipeline.__init__(self, " + self.__id__ + ", '" + self.__hmm__ + "', '" + self.__dic__ + "', '" + self.__lm__ +"')")
        self.__put__("self.__display__ = XlibUtils()")
        self.__put__("self.__active__ = True")
        self.__add_activation_conditions__(pipeline)
        self.__left__()
        self.__put__("")
        
        return True

    def __add_activation_conditions__(self, pipeline):
        activations = pipeline.findall("activation")
        
        for active in activations:
            self.__window__ = active.get("window") 
            if self.__window__ is not None:
                self.__put__("self.__window__ = '" + self.__window__ + "'")

            if active.get("mouse") == 'True':
                x = active.find("x")
                y = active.find("y")
                self.__xstart__ = x.get("start")
                self.__xend__ = x.get("end")
                
                self.__ystart__ = y.get("start")
                self.__yend__   = y.get("end")
                
                self.__put__("self.__area__ = [" + self.__xstart__ + ", " + self.__xend__ + ", " + self.__ystart__ + ", " + self.__yend__ + "]")

    def __generate_activation_function__(self, pipeline):
        activations = pipeline.findall("activation")
        sentence = "True"
        
        for active in activations:
            self.__window__ = active.get("window") 
            if self.__window__ is not None:  
                self.__put__("def __activate_on_window__(self):")
                self.__right__()
                self.__put__("if self.__display__.__compute_active_window__() == self.__window__:")
                self.__right__()
                self.__put__("return True")
                self.__left__()
                self.__put__("return False")
                self.__left__()         
                self.__put__("")
                
                sentence += " and self.__activate_on_window__()"

            if active.get("mouse") == 'True':
                self.__put__("def __activate_on_mouse__(self):")
                self.__right__()
                self.__put__("x, y = self.__display__.__compute_mouse_position__()")
                self.__put__("if self.__area__[0] <= x and  x < self.__area__[1] and self.__area__[2] <= y and y < self.__area__[2]:")
                self.__right__()
                self.__put__("return True")
                self.__left__()
                self.__put__("return False")
                self.__left__()
                self.__put__("")
                
                sentence += " and self.__activate_on_mouse__()"

        
        self.__put__("def __updateactivation__(self):")
        self.__right__()
        self.__put__("self.__active__ = " + sentence)
        self.__left__()
        

    def __generate_body__(self, pipeline):
        self.__generate_activation_function__(pipeline)
        self.__generate_process__(pipeline)

    def __generate_process__(self, pipeline):
        self.__put__("")
        self.__put__("def __process__(self, hyp, uttid):")
        self.__right__()
        self.__put__("print hyp")
        self.__put__("self.__updateactivation__()")
        self.__put__("if self.__active__ == True:")
        self.__right__()
        self.__put__("self.__send_text__(hyp)")
        self.__left__()
        self.__left__()
        self.__left__()

if __name__ == '__main__':
    pipeline_generator = PipelineGenerator(sys.argv[1])
