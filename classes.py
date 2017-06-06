# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:50:40 2017

@author: Manuel
"""

class node:
    def __init__(self, node_type, name):
        #declare allowed types
        pos_types = ["depot","sink","stop"]
        
        try:
            pos_types.index(node_type)
        except ValueError:
            raise ValueError("Only 'depot','sink','stop' are allowed")
        
        self.node_type = node_type
        self.name = name
        
        
class stop(node):
    def __init__(self, name, rec_demand):
        node.__init__(self, "stop", name)
        self.rec_demand = rec_demand
        
class depot(node):    
    def __init__(self, name, av_vehicles):
        node.__init__(self, "depot", name)
        self.av_vehicles = av_vehicles
        
class sink(node):
    def __init__(self, name):
        node.__init__(self, "sink", name)
        
class solution:       
    def __init__(self, name, routes = None):
        self.name = name
        self.route = routes