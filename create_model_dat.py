# -*- coding: utf-8 -*-
"""
Created on Tue May 23 10:18:42 2017

@author: Manuel
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:30:22 2017

@author: manuf
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 18 00:56:03 2017

@author: Manuel
"""
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import pandas as pa


#Create distance matrix from each node to each nod
def create_distance_matrix(from_nodes, to_nodes, from_name):
    ret = pa.DataFrame(from_nodes.loc[:,from_name])
    
    for i in to_nodes.index:
        dist = []
        for j in from_nodes.index:
            dist.append((vincenty((to_nodes.loc[i,"lat"],to_nodes.loc[i,"long"]), (from_nodes.loc[j,"lat"],from_nodes.loc[j,"long"])).meters)/1000)
            
        ret[to_nodes.iloc[i, 0]] = dist
        
    return ret

def get_geocoords(nodes):
    geolocator = Nominatim()
    lats = []
    longs = []
    
    for i in nodes["location"]:
        tmp = geolocator.geocode(str(i))
        lats.append(tmp.latitude)
        longs.append(tmp.longitude)
        
    nodes["lat"] = lats
    nodes["long"] = longs
    
    return nodes

def create_initial_data(path, location_alias = "location", nr_people_alias = "nr_people", depot_sample_size = None, export = True):
    
    #Necessary data import
    nodes = pa.read_csv(path + "useCase.csv", sep = ",")
    if(depot_sample_size == None):
        partner = pa.read_csv("01_Data/02_Partner/partnerReportRefactored.csv", sep = ";")
    else:
        partner = pa.read_csv("01_Data/02_Partner/partnerReportRefactored.csv", sep = ";").sample(depot_sample_size, random_state = 42)
    
    n = len(nodes)-1
    k = len(partner)
    
    #Export sampled data
    partner_info = partner.copy()
    
    #Make depots and stops comparable
    nodes = nodes.rename(columns = {location_alias: "location", nr_people_alias:"nr_people"})
    
    #Get geocoordinates of all locations
    nodes = get_geocoords(nodes)

    #Rename the sink location for convenance
    #save for potential export later on
    nodes_geo = nodes.copy()
    
    nodes.drop(["Type", "nr_people"], axis=1, inplace=True)
    partner["location"] = partner["Partner Name"]
    partner = partner[["location","lat","long"]].copy()
    
    nodes = nodes.append(partner)
    nodes.index = range(0,len(nodes))
    
    #Calculate overall distance matrix    
    dist = create_distance_matrix(nodes, nodes, "location")
    
    #set index as location
    dist.index = dist["location"].values
    #remove location & node_type
    del dist["location"]
    
    #Order rows accordingly (stops, depots, sink)
    dist = pa.concat([dist.iloc[:n,:], dist.iloc[n+1:(n+k+1),:], dist.iloc[n:n+1,:]])
    
    #Order columns according to the rows
    dist = dist[dist.index]
    
    #Export if setting is true
    if(export == True):
        partner_info.to_csv(path + "partnerReportRefactoredRed.csv", sep = ";", index = False, encoding = "utf8")
        dist.round(decimals = 2).to_csv(path + "dist.csv", sep = ";", encoding = "utf8")
        nodes_geo.to_csv(path + "useCaseGeo.csv", index = False, encoding = "utf8") #Export for visualization

    return dist, partner_info


path = "01_Data/01_UseCases/useCase1Red/"
#Create new sink

data = create_initial_data(path = path, location_alias = "Sammelpunkt in", nr_people_alias = "Anzahl Personen pro Sammelpunkt", depot_sample_size = 10)

#eport

#Create distance matrix from each start to each node
#TODO