#Complex Networks Coursework
#Simulating US power grids
#Mateusz Dubaniowski
#PhD Researcher
#Singapore-ETH Centre
#18 March 2016

import igraph
import numpy as np
import matplotlib.pyplot as plt
import random

def displayNetwork(g, visual_style={}):
    igraph.plot(g, **visual_style)
    
print ("Start simulation...")

#Importing graph
print ("Importing graph...")
g=igraph.load("power.gml", format="gml")
print ("Graph imported")

#Number of vertices and number of edges
numVer=len(g.vs)
numEdg=len(g.es)

#Variables used to keep track of totals
sum=0
prod=0
consumed=0

#Assigns the energy consumption and production values + production, - consumption.
#This is done in dimensionless units for the purpose of this simulation
counter=1
for i in g.vs:
    if counter%10==0:
        i["cap"]=20*random.randint(100, 500)
        prod=prod+i["cap"]
    else:
        i["cap"]=5*random.randint(-100, 5)
        if i["cap"]==0:
            i["cap"]=-1
        if i["cap"]>0:
            prod=prod+i["cap"]
        else:
            consumed=consumed+i["cap"]
    counter=counter+1
sum=prod+consumed

#Network energy data aggregates presented
print("Net energy value: ", sum)
print("\tEnergy produced: ", prod)
print("\tEnergy consumed: ", consumed)

#Displaying network
#print ("Displaying network...")
#displayNetwork(g)

print ("Simulation finished!")