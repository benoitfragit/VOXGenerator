#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IController:
    def get_service_status(self):
        raise NotImplementedError('subclasses must override !')

    def get_pipeline_status(self):
        raise NotImplementedError('subclasses must override !')

    def set_service_status(sefl, status):
        raise NotImplementedError('subclasses must override !')

    def set_pipeline_status(self, status):
        raise NotImplementedError('subclasses must override !')

    def get_current_plugins(self):
        raise NotImplementedError('subclasses must override !')

    def get_current_description(self):
        raise NotImplementedError('subclasses must override !')

    def set_current_description(self, f):
        raise NotImplementedError('subclasses must override !')

