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
#The graph is undirected for this simulation. The dataset supplied contains undirected graph.
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
counter=0
for i in g.vs:
    if counter%30==0:
        i["cap"]=40*random.randint(100, 500)
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

#Calculating average minimum bandwidth(capacity) of an edge
avgMinEdgeBandwidth=prod/numEdg

for i in g.es:
    i["cap"]=avgMinEdgeBandwidth

#Number of edges attached to each vertice
numEdgesAtt=[]
for i in g.vs:
    sumCon=0
    edges_attached=g.incident(i, mode="ALL")
    numEdgesAtt+=[len(edges_attached)]

#Ensuring the capacity of connections is sufficient to carry load
for i in g.vs:
    sumCon=0
    edges_attached=g.incident(i, mode="ALL")
    for j in edges_attached:
        sumCon=sumCon+g.es[j]["cap"]
    if sumCon<abs(i["cap"]):
        for j in edges_attached:
            g.es[j]["cap"]=g.es[j]["cap"]+((abs(i["cap"])-sumCon+10)/len(edges_attached))

#Printing intermediate result
for i in range(0, 10):
    print("Capacity of edge %d: %.2f" %(i, g.es[i]["cap"]))

#Total sum of capacities connected to each vertice
finalSumsCon=[]
for i in g.vs:
    sumCon=0
    edges_attached=g.incident(i, mode="ALL")
    for j in edges_attached:
        sumCon=sumCon+g.es[j]["cap"]
    finalSumsCon+=[sumCon]

#Calculating extra capacity available to each vertice
print("Extra(beyond demand) capacity available to first 21 vertices:")
extraCapacity=np.subtract(finalSumsCon, np.absolute(g.vs[:]["cap"]))
myFormattedList = [ '%.2f' % elem for elem in extraCapacity ]   #Formating doubles
print(myFormattedList[0:20], numEdgesAtt[0])                    #Printing intermediate stat

avgEdgeBandwidth=np.sum(g.es[:]["cap"])/numEdg
        
#Network energy data aggregates presented
print("Net energy value: ", sum)
print("\tEnergy produced: ", prod)
print("\tEnergy consumed: ", consumed)
print("Average initial min edge bandwidth: %.2f" % avgMinEdgeBandwidth)
print("Average edge bandwidth: %.2f" % avgEdgeBandwidth)


#Displaying network
visual_ggg={}
visual_ggg["vertex_size"] = np.add(np.divide(np.absolute(g.vs[:]["cap"]), 600), 7)
temp = np.divide(g.vs[:]["cap"], np.absolute(g.vs[:]["cap"]))
temps=[]
for i in range(0, len(temp)):
    if temp[i] > 0:
        temps+=["green"]
    else:
        temps+=["red"]
visual_ggg["vertex_color"] = temps
visual_ggg["edge_curved"] = 0
visual_ggg["edge_width"] = 0.75
#print ("Displaying network...")
displayNetwork(g, visual_ggg)

print ("Simulation finished!")