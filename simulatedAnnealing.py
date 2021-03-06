# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 01:49:18 2017

@author: Manuel
"""

import time

#SIMULATED ANNEALING
def simulatedAnnealing(sol, T0 = None, Te = None, c = None, K = None, N = None, timeMax = 60):
    """
    Method of improving the initial solutions generated by the construction heuristic
    
    Initial temperature:
        According to our experience, those parameters shall take size of input 
        instances into account, otherwise the tuned solver will very likely 
        perform badly when applied to new instances with different input size.
        
        The T0 determine the tolerance of worse moves in the initial phase. We set
        it to the average distance of routes in the initial solution produced by RBI.
        
    Termination temperature:
        
    ___________________________________________________________________________
    sol:    Initial solution generated by randomizedBestInsertion
    T0:     Initial temperature
    Te:     Termination temperature
    c:      Cooling ratio
    K:      Number of iterations at given temperature
    N:      Number of maximum unsuccessfull given attempts at given temperature
    timeMax:Time the annealing approach is allowed to run at most. (default = 60 secs)
    
    ___________________________________________________________________________
    """
    
    
    #Set default parameters #MISSING!
    if(T0 = None):
        T0 = None
        
    if(K = None):
        K = None
    
    t = T0
    best = sol.copy()
    
    start = time.time()
    
    while(t < Te and (time.time() < start + timeMax)):
        i = 0
        n = 0
        while(i < K and n < N):
            #r1 4.6 ← randomly choose a route from S;
            r1 = random.choice(sol)
            #r2 4.7 ← randomly choose a route from S;
            r2 = random.choice(sol)
            
            #4.8 randomly select a sub-route sr1 from r1;
            start_ind, stop_ind, rndSubroute = randomSubRoute(r1)
            
            if(r1 == r2):
                #4.10 generate a random real number p ∈ [0, 1];
                #4.11 len ← number of nodes on r1;
                #4.12 if p < 1/len then
                if(random.uniform(0,1) < (1/len(r1))):                    
                    #4.13 move sub-route sr1 to a different random location on r1;
                    r1 = randomSubRouteReallocation(r1, rndSubroute)
                else:
                    #4.15 randomly select a different non-overlapping sub-route sr2;
                    #randomly select a random subroute either before or behind the orignial route
                    tmp = random.choice([randomSubRoute(r1[:start_ind]), randomSubRoute(r1[:stop_ind]))
                    start_ind2, stopt_ind2, rndSubroute2 = tmp
                    
                    #4.16 swap sr1 with sr2;
                    if(start_ind > start_ind2):
                        route = route[:start_ind2] + rndSubroute + route[stop_ind2:start_ind] + rndSubRoute2 + route[stop_ind:]
                    else:
                        route = route[:start_ind] + rndSubroute2 + route[stop_ind:start_ind2] + rndSubRoute1 + route[stop_ind2:]
                    
                    
            else:               
                #4.19 generate a random real number p ∈ [0, 1];
                #4.20 len ← number of routes in S;
                #4.21 if p < 1/len then
                #4.22 move sub-route sr1 to a random location on r2, if the
                #capacity constraint is not violated.;
                #4.23 else
                #4.24 randomly select s sub-route sr2 from r2;
                #4.25 swap sr1 with sr2, if the capacity constraints are not
                #violated.;
                #4.26 end
                #4.27 end
            
    
    return None


def randomSubRouteReallocation(route, subroute):
    #remove subroute from route
    tmp_route = [x for x in route if x not in subroute]
    start_int = random.randint(0,len(tmp_route))
    tmp_route = tmp_route[:start_int] + subroute + tmp_route[start_int:]
    
    return tmp_route

def randomSubRoute(route):
    n = len(route)
    i1, i2 = 1, 2
    rndSubroute = []
    
    while(i1 != i2):
        #IMPORTANT, depot and sink have to be unfazed by the changes
        i1 = random.randint(1,n-2)
        i2 = random.randint(1,n-2)
        
        rndSubroute = route[min([i1,i2],max(i1,i2))]
    
    return min([i1, i2]), max([i1,i2]), rndSubroute