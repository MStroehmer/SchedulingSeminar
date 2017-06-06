# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 01:43:45 2017

@author: Manuel
"""

import randomizedBestSolution as rbs
import simulatedAnnealing as sa
import TSPoptimization as opt

#Overall solver

def overall_solver(s, C, D, g, maxCap = 50, maxTimeH = 8, avg_speed = 70, lmd = 0.05):
    
#    3.1 S0 ← RandomizedBestInsertion(C,D,g);
    first_solution = rbs.randomizedBestInsertion(s, C, D, g, maxCap = maxCap, maxTimeH = maxTimeH, avg_speed = avg_speed, lmd = lmd)
    
    #3.2 S ← SimulatedAnnealing(S0);
    #MISSING
    
    #Optimize every route again after performing the simulated annealing approach
    opt_sol = []
    
    for route in first_solution:
        route = opt.optimizeRoute(route, g)
        opt_sol.append(route)
        
    return opt_sol