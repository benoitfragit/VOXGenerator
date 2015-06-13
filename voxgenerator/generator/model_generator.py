#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from lxml import etree

class ModelGenerator:
    def __init__(self, xml, lms):
        base = os.path.dirname(lms)
        
        if not os.path.isdir(base):
            os.mkdir(base)
        
        if os.path.isfile(xml):
            plugin_tree = etree.parse(xml)
            plugins = plugin_tree.xpath("/plugins/plugin")

            lmctl = open(lms, "w")

            for plugin in plugins:
                commands = plugin.findall("command") 
                name = plugin.get("name")
  
                filepath = base + "/" + name + "_raw.txt"
                modelpath = base + "/" + name + ".lm.dmp"
                f = open(filepath, "w")
                
                for cmd in commands:
                    transcript = cmd.get("transcription")
                    
                    if transcript is not None:
                        line = "<s> " + transcript + " </s>\n"
                        f.write(line)
                
                f.close()
                
                self.__buildmodel__(base, name, filepath)
                lmctl.write(modelpath + " " + name + "\n")
            
            lmctl.close()
        else:
            print "XML plugin file " + xml + " is not valid !"

    def __buildmodel__(self, b, name, tmpfile):
        base = b + "/" + name
        vocab = base + '.vocab'
        idngram = base + '.idngram'
        arpa = base + '.arpa'
        lm = base + '.lm.dmp'
        
        os.system('text2wfreq < ' + tmpfile + ' | wfreq2vocab > ' + vocab)
        os.system('text2idngram -vocab ' + vocab + ' -idngram ' + idngram  + ' < ' + tmpfile)
        os.system('idngram2lm -vocab_type 0 -idngram ' + idngram + ' -vocab ' + vocab + ' -arpa ' + arpa)
        os.system('sphinx_lm_convert -i ' + arpa + ' -o ' + lm)

        os.remove(vocab)
        os.remove(idngram)
        os.remove(arpa)

        print 'Language model has been written in ' + lm    
    

if __name__ == '__main__':
    model_generator = ModelGenerator(sys.argv[1])
