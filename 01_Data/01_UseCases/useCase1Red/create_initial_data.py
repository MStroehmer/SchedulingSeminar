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

path = "01_Data/01_UseCases/useCase1Red/"

nodes = pa.read_csv(path + "useCase.csv", sep = ",")
partner = pa.read_csv("01_Data/02_Partner/partnerReportRefactored.csv", sep = ";").sample(10, random_state = 42)

n = len(nodes)-1
k = len(partner)

#Export sampled data
partner.to_csv(path + "partnerReportRefactoredRed.csv", index = False, encoding = "utf8")

nodes = nodes.rename(columns = {"Sammelpunkt in": "location", "Anzahl Personen pro Sammelpunkt":"nr_people"})

#Create new sink
sink = "Reimboldshäuser Straße 1, 36275 Kirchheim"

#Get geocoordinates of all locations
geolocator = Nominatim()
lats = []
longs = []

for i in nodes["location"]:
    tmp = geolocator.geocode(str(i))
    lats.append(tmp.latitude)
    longs.append(tmp.longitude)
    
nodes["lat"] = lats
nodes["long"] = longs

nodes["location"][nodes["Type"] == "Sink"] = "Sink"

#Export for visualization
nodes.to_csv(path + "useCaseGeo.csv", index = False, encoding = "utf8")

nodes.drop(["Type", "nr_people"], axis=1, inplace=True)
partner["location"] = partner["Partner Name"]
partner = partner[["location","lat","long"]].copy()

nodes = nodes.append(partner)
nodes.index = range(0,len(nodes))

#Create distance matrix from each node to each nod
def create_distance_matrix(from_nodes, to_nodes, from_name):
    ret = pa.DataFrame(from_nodes.loc[:,from_name])
    
    for i in to_nodes.index:
        dist = []
        for j in from_nodes.index:
            dist.append((vincenty((to_nodes.loc[i,"lat"],to_nodes.loc[i,"long"]), (from_nodes.loc[j,"lat"],from_nodes.loc[j,"long"])).meters)/1000)
            
        ret[to_nodes.iloc[i, 0]] = dist
        
    return ret

#node + depots

#Calculate overall distance matrix    
dist = create_distance_matrix(nodes, nodes, "location")

#Order the columns of the dataframe accordingly (nodes, depot, sink)
tmp = dist[list(dist.columns[dist.columns != "Sink"])].copy()
dist = tmp.assign(Sink = dist["Sink"]).copy()


#Order the dataframe accordingly (nodes, depot, sink)
n_index = list(range(0,n)) + [n+k] + list(range(n,n+k))
dist.index = n_index
dist.sort_index(inplace = True)

dist.round(decimals = 2).to_csv("01_Data/01_UseCases/useCase1Red/dist.csv", sep = ";", index = False, encoding = "utf8")

#Create distance matrix from each start to each node
#TODO