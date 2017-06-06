# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 20:08:15 2017

@author: Manuel
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:57:25 2017

@author: Manuel
"""

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt


#path = "01_Data/01_UseCases/useCase1/"
path = "01_Data/01_UseCases/useCase1Red/"


def solution_viz(solution, partner_info, useCaseGeo):   
    #CREATE PLOT OUTLINE
    fig = plt.figure(figsize=(26, 18))
    #fig = plt.figure(figsize=(20, 14))
    fname = '01_Data/03_Cartopy/DEU_adm_shp/DEU_adm1.shp'
    
    adm1_shapes = list(shpreader.Reader(fname).geometries())
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    plt.title('Deutschland')
    #10m coastline parsing for good resolution
    ax.coastlines(resolution='10m')
    ax.set_extent([4, 16, 47, 56], ccrs.PlateCarree())
    
    ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                      edgecolor='black', facecolor='gray', alpha=0.3)
    
    
    
    #Add all locations we have to address in blue triagles
    ax.scatter(useCaseGeo["long"][:-1], useCaseGeo["lat"][:-1],
               transform=ccrs.Geodetic(), color = "blue", marker = "v", s = 100)
    
    #Add all buspartner depots in green dots
    ax.scatter(partner_info["long"], partner_info["lat"], 
               transform=ccrs.Geodetic(), color = "green", s = 100, alpha = 0.7)
    
    #Paint the sink as a red cross
    ax.scatter(useCaseGeo["long"][-1:], useCaseGeo["lat"][-1:],
               transform=ccrs.Geodetic(), color = "red", marker = "X", s = 200)
    
    #plot all routes
    for x in solution:
        for i in range(len(x)-1):
            #if node is a depot, get the line from partner_info
            prec = x[i]
            post = x[i+1]
            
            
            if(prec.node_type == "depot"):
                lat1 = partner_info[partner_info["Partner Name"] == prec.name]["lat"].values
                long1 = partner_info[partner_info["Partner Name"] == prec.name]["long"].values
            if(post.node_type == "depot"):
                lat2 = partner_info[partner_info["Partner Name"] == post.name]["lat"].values
                long2 = partner_info[partner_info["Partner Name"] == post.name]["long"].values
                
                
            #if node is a stop, get 
            if(prec.node_type != "depot"):
                lat1 = useCaseGeo[useCaseGeo["location"] == prec.name]["lat"].values
                long1 = useCaseGeo[useCaseGeo["location"] == prec.name]["long"].values
            if(post.node_type != "depot"):
                lat2 = useCaseGeo[useCaseGeo["location"] == post.name]["lat"].values
                long2 = useCaseGeo[useCaseGeo["location"] == post.name]["long"].values

            plt.plot([long1, long2], [lat1, lat2],
                     color="black", linewidth = 3,
                     transform=ccrs.PlateCarree()
                     )

            
    fig.show()
