# VOXGenerator

Rapidly create powerfull voice controlled app on your desktop.

## What is VOXGenerator

VOXGenerator is a python package based on pocketsphinx to provide offline voice controlled support on your desktop. It's goal is to make the user able to create powerfull voice recognition app by only writting xml.

### How it works

Users only have to write a file to contains its plugins and a file to describe the pipeline.

#### What is a plugin ?

```xml
<?xml version="1.0"?>
<plugins>
	<plugin id="0" name="Open" reload="False" ip="127.0.0.1" port="5100">
		<package name="test"  module="module"/>
		<command name="documents" transcription="ouvre mes documents" type="system" exec="ls"/>
		<command name="musiques"  transcription="ouvre ma musique" type="custom"/>
		<command name="images"    transcription="ouvre mes images" type="custom"/>
	</plugin>
    <plugin id="1" name="Action" reload="False" ip="127.0.0.1" port="6000">
		<command name="copier" transcription="copier ceci" type="system" exec="xdotool key ctrl+c"/>
		<command name="coller" transcription="coller ici"  type="system" exec="xdotool key ctrl+v"/>
		<command name="couper" transcription="couper ceci" type="system" exec="xdotool key ctrl+x"/>
	</plugin>
</plugins>
```
Each plugin is described like this:

``` xml
	<plugin id="0" name="Open" reload="False" ip="127.0.0.1" port="5100">
		<package name="test"  module="module"/>
		<command name="documents" transcription="ouvre mes documents" type="system" exec="ls"/>
		<command name="musiques"  transcription="ouvre ma musique" type="custom"/>
		<command name="images"    transcription="ouvre mes images" type="custom"/>
	</plugin>
```
A plugin generator is going to parse this description and create a python plugin

``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from voxgenerator import Plugin
class Open(Plugin):
    def __init__(self):
        Plugin.__init__(self, '127.0.0.1', 5100)
        self.__id__ = 0
        self.__name__ = 'Open'

        self.__function__[0] = self.documents
        self.__function__[1] = self.musiques
        self.__function__[2] = self.images
        
        self.__command__[0] = 'ouvre mes documents'
        self.__command__[1] = 'ouvre ma musique'
        self.__command__[2] = 'ouvre mes images'
        
        self.__build__('Open', False)
        self.__receive__()
    
    def documents(self):
        os.system('ls')
    
    def musiques(self):
        raise NotImplementedError('subclasses must override musiques()!')
    
    def images(self):
        raise NotImplementedError('subclasses must override images()!')
    
    def __process__(self, name, hyp):
        if self.__name__ == name:
            print 'Plugin ' + name + ' receive : '+ hyp
            idx = self.__selector__.__query__(hyp)
            if self.__function__.has_key(idx):
                self.__function__[idx]()

if __name__ == '__main__':
    p = Open()

```

Each plugin works as a standolone app and can be deployed on each computer you want. Each plugin communicates with a voice recognition pipeline using TCP.  If you want to start a plugin you should call the __receive__ function like this:

``` python
plugin.__receive__()
```
Then the plugin is going to wait for voice transcription from the voice pipeline.  The __receive__ function is going to call the __process__ function.

Each plugin could have system commands and custom command.
System command will directly be executed if the corresponding function start. Custom commands should be overwritten by child class that inherit plugin class.

#### How to describe a pipeline ?

The pipeline should be describe in a xml file like this:

``` xml
<?xml version="1.0"?>
<pipelines>
	<dic     file="/home/benoit/PyGNUVoice/sphinx/dictionnary.dic"/>
	<hmm     file="/home/benoit/PyGNUVoice/sphinx/hmm"/>
	<include file="/home/benoit/PyGNUVoice/plugin.xml"/>
	<lmctl   file="/home/benoit/PyGNUVoice/lm/lmctl.txt"/>
	
	<pipeline priority="1" plugin="Open" ip="127.0.0.1" port="5100">
		<activation window="chrome"/>
		<activation mouse="True">
			<x start="0" end="200"/>
			<y start="0" end="200"/>
	    </activation>
		<activation keyword="Jasper"/>
    </pipeline>
   	<pipeline default="True" priority="0" plugin="Action" ip="127.0.0.1" port="6000"/>
</pipelines>

```

Each pipeline is going to work with one plugin.  A langage model controller make it easy to switch between plugin thanks to activation. The activated pipeline with the highest priority is going to send text to its associated plugin.

Be sure to include the file containing the list of available plugins descriptions.

When you launch a Pipeline then a versioning system is going to launch a plugin generation, langage model generation and a langage control file generation so that user as nothing else to do than launching a pipeline.
