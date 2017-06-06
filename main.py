# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:52:19 2017

@author: Manuel
"""

import pandas as pa

#Import related project imports
import classes as classes
import randomizedBestSolution as rbs
import solutionViz as viz
import importlib

#Randomized best insertion algorithm
            
importlib.reload(rbs)
importlib.reload(viz)


#import
path = "01_Data/01_UseCases/useCase1/"


def main(path):
    #1) IMPORT
    dist = pa.read_csv(path + "dist.csv", index_col = 0, sep = ";")
    useCaseGeo = pa.read_csv(path + "useCaseGeo.csv")
    partner_info = pa.read_csv(path + "partnerReportRefactored.csv", sep = ";")

    #2) INITIALIZATION
    #Initialize all stops
    stops = useCaseGeo[useCaseGeo["Type"] == "Stop"]
    stops = [classes.stop(stops["location"].iloc[i], stops["nr_people"].iloc[i]) for i in range(0, len(stops))]
    #Initialize all depots
    depots = [classes.depot(partner_info["Partner Name"].iloc[i], partner_info["Vehicles Given"].iloc[i]) for i in range(0, len(partner_info))]
    #Initialize the sink
    sinks = str(useCaseGeo[useCaseGeo["Type"] == "Sink"]["location"].values[0])
    sinks = classes.sink(sinks)
    
    #3) SOLVE
    solutions = rbs.randomizedBestInsertion(s = sinks, C = stops, D = depots, g = dist, maxTimeH = 12)
    
    #4) ANALYSE THE SOLUTION
    for x in solutions:
        print([y.name for y in x])
        
    #plot the solution route
    viz.solution_viz(solutions, partner_info, useCaseGeo)
        
    
main(path)