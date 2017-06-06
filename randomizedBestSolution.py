# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:35:46 2017

@author: Manuel
"""

import random
from classes import *
import TSPoptimization as opt
random.seed(42)


#Randomized best insertion algorithm
#Missing a good estimation for delta
def randomizedBestInsertion(s, C, D, g, maxCap = 50, maxTimeH = 8, avg_speed = 70, lmd = 0.05):
    """
    High level function for the randomized best insertion part of the heuristic
    ___________________________________________________________________________
    s: Sink to which every bus needs to connect
    C: Set of "customers" in the paper  (stops in bus implementation)
    D: Set of "depots"
    g: graph in the paper               (distance matrix in implementation)
    maxCap: maximum capacity of a bus
    maxTimeH: maximum time that a bus is allowed to drive
    avg_speed: Average speed of every bus on that route (for driving time)
    ___________________________________________________________________________
    """
    
    #Create working clones
    tmp_C, tmp_D = C.copy(), D.copy()

    solution = []

    #line 1.2, initilize loop
    while(tmp_C != []):
            #line 1.3-1.6, initialize solution
            tmp_C, tmp_D, route = initializeRoute(s, tmp_C, tmp_D, g)
                
            #Check if route exceeds the driving time, throw exception if it does
            if(checkRouteTime(g, route, maxTimeH, avg_speed) == False):
                raise Warning("At least one stop can not be inclueded within the maximum driving time")
                return None
            
            #line 1.7, initialize repeat
            while(True):
                
                #line 1.9 initialize c2Max, bestC and bestR                
                c2Max, bestC, bestR = float("-inf"), None, None
                
                #line 1.10 for loop
                for c in tmp_C:
                    tmp_route = route.copy()
                    #line 1.11 if adding c to r does not violate capacity constraint
                    #line 1.11 ADDITION: if adding c to r does not violate the best case duration
                    if(checkRouteFeas(c, route, g, maxCap)):
                        
                        #line 1.12 initialize c1Min and clv
                        c1Min, clv = float("inf"), None
                        
                        
                        #line 1.13: As the route is optimized either way, insert the new node after the depot
                        #line 1.13, foreach consecutive pair of nodes (u, v) on route r
                        
                        #OUTDATED:  insertion poisition is not relevant when optimizing the route eitherway.
#                        for i in range(0, len(route)-1):
#                            #line 1.14, c1 ← g(u, c) + g(c, v) − g(u, v);
#                            #g(u, c)
#                            m1 = g.loc[route[i].name, c.name]
#                            #g(c, v)
#                            m2 = g.loc[c.name, route[i+1].name]
#                            #g(u, v)
#                            m3 = g.loc[route[i].name, route[i+1].name]
#                            
#                            c1 = m1 + m2 - m3
#                    
#                            #line 1.15: if c1 < c1Min then c1Min ← c1, c1v ← v
#                            if(c1 < c1Min):
#                                c1Min = c1
#                                clv = route[i+1]

                        #line 1.17: r1 ← insert c into route r before c1v;
#                        ind = route.index(clv)
                        #insert the new node behind the depot and be 
                        tmp_route.insert(1, c)
                        
                        #1.18 r2 ← OptimizeRoute(r1, index of c1v);
                        opt_route = opt.optimizeRoute(tmp_route, g)
                        
                        #1.19 δ ← the difference between total distance of r2 and r;
                        delta = getRouteDistance(tmp_route,g) - getRouteDistance(opt_route, g)
                        
                        #1.20 d ← neariest depot to customer c;
                        d = getNearestDepot(c, D, g)
                        
                        
                        #1.21 c2 ← λ · (g(d, c) + g(c, d)) − δ;
                        #Anotation: g(d,c) == g(c,d) -> 2x g(d,c)
                        c2  = lmd *(g.loc[d.name, c.name] + g.loc[c.name, d.name]) - delta
                        
                        #line 1.22 (check if the newly defined optimal route is time feasible)
                        #As the optimal route is also the shortest route -> no subroute is feasible if the optimum is not
                        #Work over it!!
                        if(checkRouteTime(g, tmp_route, maxTimeH, avg_speed) == False):
                                continue
                            
                        #1.22 if c2 > c2Max then c2Max ← c2, bestC ← c,
                        if(c2 > c2Max):
                            c2Max = c2
                            bestC = c
                            bestR = opt_route
                                              
                        
                  
                #1.25 if bestC != null then r ← bestR, delete bestC from C ;
                if(bestC != None):
                    route = bestR
                    tmp_C.remove(bestC)
                
                #1.26 break repeat when necessary
                if(bestC == None):
                    break
                
                
            #1.27 add r to Solution S;
            solution.append(route)
    
    return solution
    

def checkRouteFeas(node, route, g, maxCap):
    """
    Low level helper function to check if a route obeyes the set limitations.
    
    ___________________________________________________________________________
    
    route: route that needs to be checked
    g: graph in the paper               (distance matrix in implementation)
    maxCap: maximum capacity of a bus
    maxTimeH: maximum time that a bus is allowed to drive
    ___________________________________________________________________________
    """
    
    #1) the route needs to start with a depot
    if(route[0].node_type != "depot"):
        return False
    
    
    #2) the route needs to end with the SAME depot
    if(route[0] != route[-1]):
        return False
    
    
    #3) the sum of the rec_demand should no exceed the max capacity of the bus
    if((sum([x.rec_demand for x in route if x.node_type == "stop"])+node.rec_demand) > maxCap):
        return False
    
    
    return True

def checkRouteTime(g, route, maxTimeH, avg_speed): 
    
    if(getRouteTime(route, g, avg_speed) > maxTimeH):
        return False
    
    return True
    
def getRouteDistance(route, g):
    prec = None
    distance = 0
    
    for x in route:
        #skip the first entry:
        if(prec == None):
            prec = x
            continue
            
        distance = distance + g.loc[x.name,prec.name]
        prec = x
        
    return distance
        
        

def getRouteTime(route, g, avg_speed):
    distance = getRouteDistance(route, g)
    time = distance/avg_speed
        
    return time

def getNearestDepot(c, D, g):
    #get the column of our location
    column = g[c.name].copy()

    #select only only depots with free capacity out of t
    depot_names = [x.name for x in D if x.av_vehicles > 0]
    column = column.loc[depot_names]   
    
    #get the depot of the closest depot
    depot_name = column.idxmin()
    d = next((x for x in D if x.name == depot_name), None)
        
    
    return d
    
def initializeRoute(s, C, D, g):
    """
    line 1.3 - 1.6 of the "Randomized best insertion algorithm" of the paper
    
    ___________________________________________________________________________
    
    C: Set of "customers" in the paper  (stops in bus implementation)
    D: Set of "depots"
    g: graph in the paper               (distance matrix in implementation)
    ___________________________________________________________________________
    
    """
    
    
    #Create working clones
    tmp_C, tmp_D, tmp_g = C.copy(), D.copy(), g.copy()
    
    #1.3 Randomly choose a customer c, and delete it from C
    c = random.choice(tmp_C)
    tmp_C.remove(c)
    
    #1.4 Find neariest depot d from D for c that has available vehicle(s)
    d = getNearestDepot(c, tmp_D, tmp_g)
    
    #1.5 Construct a route r consisting of three nodes [d, c, d]
    #ADDITION add the sink before the last depot [d,c,s,d]
    route = [d,c,s,d]
    
    #1.6.1 decrease number of vehicles available at d by one
    d.av_vehicles = d.av_vehicles-1

            
    return tmp_C, tmp_D, route
    