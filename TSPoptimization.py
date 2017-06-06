# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:57:15 2017

@author: Manuel
"""

from gurobipy import *
import pandas as pa
import numpy as np

#OPTIMIZE ROUTE of the traveling salesman problem

#Sniedovich M. - A dynamic programming algorithm for the travelling salesman
#problem APL Quote Quad, 23(4), 1-2, 1993

def optimizeRoute(route, g):
    """
    Helper method for optimizing the route after insertion
    
    ___________________________________________________________________________
    route: Route to be optimized
    i: location where a new customer is just inserted
    w: number of nodes to be optimized at once
    ___________________________________________________________________________
    """
    
    tmp_g = graphReduction(route, g)

    
    m = TSPsolver(tmp_g)

    tmp_route = resultInterpreter(route, m, tmp_g)
    
    return tmp_route
    


def graphReduction(route, g):
    """
    Low level helper function to:
        - remove all unnecessary stops from the distance matrix
        - position the depot in first place
        - position the sink in last place
    """
    
    
    #get all node names and only unique entries
    names = list(set([x.name for x in route]))
    
    #reduce lines
    tmp_g = g.loc[names,:].copy()
        
    #reduce columns
    tmp_g = tmp_g[names]
    
    #set depot on first row
    #get index of the depot
    ind = int(np.where(tmp_g.index == route[0].name)[0])
    tmp_g = pa.concat([tmp_g.iloc[ind:ind+1, :], tmp_g.iloc[:ind, :], tmp_g.iloc[ind+1:, :]])
    
    #set the sink to the last row
    ind = int(np.where(tmp_g.index == route[-2].name)[0])
    tmp_g = pa.concat([tmp_g.iloc[:ind, :], tmp_g.iloc[ind+1:, :], tmp_g.iloc[ind:ind+1, :]])
    
    #Order the columns according to the rows
    tmp_g = tmp_g[tmp_g.index]
    
    return tmp_g


def TSPsolver(g):
    """
    linear programm modeled and solved in gurobi for a simple traveling salvesman problem
    It is important that the depot is i,j = 0
    It is important that the sink is i,j = n-1
    
    ___________________________________________________________________________
    g: reduced search graph done by the route
    ___________________________________________________________________________   
    """
    n = len(g)
    
    #solve the subproblem optimaly with linear programming
    m = Model("TSP")
    
    #Mute the output of gurobi
    m.setParam('OutputFlag', 0) 
    
    x_raw = tuplelist([(i,j) for i in range(n) for j in range(n)])
    x = m.addVars(x_raw, vtype=GRB.BINARY, name = "x")
    
    u_raw = tuplelist(i for i in range(n))
    u = m.addVars(u_raw, vtype = GRB.INTEGER, name = "u")
    
    
    obj = quicksum(quicksum(g.iloc[i,j]*x[i,j] for i in range(n)) for j in range(n))
    m.setObjective(obj, GRB.MINIMIZE)
    
    #For each trip, there is a followup trip (1)
    visit_once = m.addConstrs((x.sum(i, range(n)) == 1
                           for i in range(n)), "visit_once")

    #Each trip is visited (2)
    no_static_vis = m.addConstrs((x.sum(range(n), j) == 1
                        for j in range(n)), "no_static_vis")
    
    #Force follow up and remove subcycle (3)
    m.addConstrs(u[i] - u[j] + n*x[i,j] <= n-1
                 for i in range(1, n) for j in range(1, n))
    
    #Force the diagonal to 0 (4)
    force_diag = m.addConstrs((x[i,i] == 0
                         for i in range(0,n)), "force_diag")
    
    #Force sink to depot
#    sinkDep = m.addConstrs((x.sum(range(n-1,n), j) == 1
#                           for j in range(0,1)), "sink_to_depot")
    
    sinkDep = m.addConstr(x[n-1,0] == 1, "sink_to_depot")
    
    m.update()
    m.optimize()
    
    return m

def resultInterpreter(route, m, g):
    """
    Low level helper function to interpret the traveling salesman problem solution
    by gurobi
    
    ___________________________________________________________________________   
   
     m: reduced search graph done by the route
    ___________________________________________________________________________   
    """

    
    n = len(route)-1
    #get all x and reshape the results
    x_opt = [i.X for i in m.getVars()][:n**2]
    
    x_opt = pa.DataFrame(np.array(x_opt).reshape(n, n), index = g.index, columns = g.columns)
    
    #interpret the results, start from the depot
    from_node_name = route[0].name
    #initialize the route from the depot
    opt_route = [route[0]]
    
    while(len(opt_route) != len(route)):
        #get the name of the next stop and find the corresponding note in the previous route
        to_node_name = x_opt.loc[from_node_name,:][x_opt.loc[from_node_name,:] == 1].index[0]
        to_node = [x for x in route if x.name == to_node_name][0]
        
        #add to the new route
        opt_route.append(to_node)
        #step one step further
        from_node_name = to_node_name

    return opt_route
