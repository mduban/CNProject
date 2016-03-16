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
import sys

def displayNetwork(g, visual_style={}):
    igraph.plot(g, **visual_style)

#Displaying network
def displayGraph(g):
    visual_ggg={}
    visual_ggg["vertex_size"] = np.add(np.divide(np.absolute(g.vs[:]["capCur"]), 600), 7)
    temp = np.divide(g.vs[:]["capCur"], np.absolute(g.vs[:]["capCur"]))
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

#This function balances a network supplied to the function
def balanceNetwork(g, MAXCHNG):
    err=0
    allPos=0
    allNeg=0
    totAvCap=prod
    maxChng=prod
    xover=1
    while allPos==0 and allNeg==0 and maxChng>MAXCHNG and xover==1:
        if err>0:
            break
        allPos=1
        allNeg=1
        maxChng=0
        xover=0
        for i in g.es:
            v1=i.source
            v2=i.target
            caps=[g.vs[v1]["capCur"], g.vs[v2]["capCur"]]
            avg=(g.vs[v1]["capCur"]+g.vs[v2]["capCur"])/2
            chng=-np.subtract(caps, [avg, avg])
            capI=i["cap"]
            inc1=g.vs[v1]["attCapUsed"][i.index]+chng[0]
            inc2=g.vs[v2]["attCapUsed"][i.index]+chng[1]
            inc1=round(inc1, 3)
            inc2=round(inc2, 3)
            avg=round(avg, 3)
            chng[0]=round(chng[0], 3)
            chng[1]=round(chng[1], 3)
            if abs(inc1)-abs(inc2)>0.01:
        	    print("Error! Numerical. Rounding exceeded.", abs(inc1)-abs(inc2))
        	    err=1
        	    break
            inc=abs(inc1)
            if capI>=inc:
        	    g.vs[v1]["capCur"]+=chng[0]
        	    g.vs[v2]["capCur"]+=chng[1]
        	    g.vs[v1]["attCapUsed"][i.index]=inc1
        	    g.vs[v2]["attCapUsed"][i.index]=-inc1
            else:
        	    if inc1>0:
        		    inc1=capI
        		    inc2=-capI
        	    else:
        		    inc1=-capI
        		    inc2=capI
        	    chng[0]=inc1-g.vs[v1]["attCapUsed"][i.index]
        	    chng[1]=inc2-g.vs[v2]["attCapUsed"][i.index]
        	    inc1=round(inc1, 3)
        	    g.vs[v1]["attCapUsed"][i.index]=inc1
        	    g.vs[v2]["attCapUsed"][i.index]=-inc1
        	    g.vs[v1]["capCur"]+=chng[0]
        	    g.vs[v2]["capCur"]-=chng[0]
        	    g.vs[v1]["capCur"]=round(g.vs[v1]["capCur"], 3)
        	    g.vs[v2]["capCur"]=round(g.vs[v2]["capCur"], 3)
            if g.vs[v1]["capCur"]<0 or g.vs[v2]["capCur"]<0:
        	    allPos=0
            if g.vs[v1]["capCur"]>=0 or g.vs[v2]["capCur"]>=0:
        	    allNeg=0
            if abs(chng[1])>maxChng:
                maxChng=abs(chng[1])
            if abs(chng[0])>maxChng:
                maxChng=abs(chng[0])
            if (caps[0]<=0 and g.vs[v1]["capCur"]>=0) or (caps[1]<=0 and g.vs[v2]["capCur"]>=0):
                xover=1
            if (caps[0]>=0 and g.vs[v1]["capCur"]<=0) or (caps[1]>=0 and g.vs[v2]["capCur"]<=0):
                xover=1
            i["capCur"]=abs(inc1)
        for h in g.vs:
            tempsum=0
            for hh in h["att"]:
                tempsum=tempsum+g.es[hh]["cap"]-max(0, h["attCapUsed"][hh])
            if (h["capCur"]+tempsum)<0:
                print("Error! System unbalancable.")
                err=2
                break
            tempsum=0
            for hh in h["att"]:
                tempsum=tempsum+g.es[hh]["cap"]+min(0, h["attCapUsed"][hh])
            if (h["capCur"]-tempsum)>0:
                totAvCap-=(h["capCur"]-tempsum)
            if totAvCap<-consumed:
                print("Error! System unbalancable.")
                err=2
                break
        print(maxChng)
            
    print(totAvCap-consumed, v1, v2, avg, caps, chng, capI, i.index, inc1, inc2, inc)
    print(allPos, allNeg, maxChng)
    
    #Printing info on the network state
    allPos=1
    balanced=False
    for i in g.vs:
        if i["capCur"]<0:
            #print("ID: ", i["id"], " Cap: ", i["capCur"])
            allPos=0
    if allPos==1:
        print("All vertices are satisfied!")
        balanced=True
    if allNeg==1:
        print("Not enough load")
    if allNeg==0 and allPos==0:
        print("System unbalancable")
    if xover==0 and not balanced:
        print("No crossover!")
    return [g, balanced]
    
print ("Start simulation...")

MAXCHNG=0.99

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
    i["capCur"]=i["cap"]
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

#Adjust the connection capacity
for i in g.es:
    i["cap"]*=20

#Printing intermediate result
for i in range(0, 10):
    print("Capacity of edge %d: %.2f" %(i, g.es[i]["cap"]))

#Total sum of capacities connected to each vertice
finalSumsCon=[]
for i in g.vs:
    sumCon=0
    edges_attached=g.incident(i, mode="ALL")
    i["att"]=edges_attached
    temp=g.es[edges_attached]["cap"]
    for j in range(0, len(temp)):
        temp[j]=0
    i["attCapUsed"]=dict(zip(i["att"], temp))
    for j in edges_attached:
        sumCon=sumCon+g.es[j]["cap"]
    finalSumsCon+=[sumCon]

#Balance the network
[g, balanced]=balanceNetwork(g, MAXCHNG)

#Calculating extra capacity available to each vertice
print("Extra(beyond demand) capacity available to first 21 vertices:")
extraCapacity=np.subtract(finalSumsCon, np.absolute(g.vs[:]["capCur"]))
myFormattedList = [ '%.2f' % elem for elem in extraCapacity ]   #Formating doubles
print(myFormattedList[0:20], numEdgesAtt[0])                    #Printing intermediate stat

avgEdgeBandwidth=np.sum(g.es[:]["cap"])/numEdg
extraTotalBandwidth=np.sum(g.es[:]["cap"])-np.sum(g.es[:]["capCur"])

#Network energy data aggregates presented
print("Net energy value: ", sum)
print("\tEnergy produced: ", prod)
print("\tEnergy consumed: ", consumed)
print("Average initial min edge bandwidth: %.2f" % avgMinEdgeBandwidth)
print("Average edge bandwidth: %.2f" % avgEdgeBandwidth)
print("Extra bandwidth available in the whole network: ", extraTotalBandwidth)

#Edges at peak bandwidth
peakBandwidth=[]
for i in g.es:
    if i["capCur"]>=0.9*i["cap"]:
        peakBandwidth+=[i.index]
print("Edges close to or at peakBandwidth: ", peakBandwidth)

#displayGraph(g)

if not balanced:
    sys.exit()
#Up to here we set up a network with given capacities.
#Now, we will attempt to break it and see what happens.
#Whether we can maintain supply of electricity to each vertice after nodes are removed.
#This is initial estimate looking just at peak energy transfer. This is considering full inward transfer.

nodeToRemove=random.randint(0, numVer)
print("We will remove node: ", nodeToRemove)

g.delete_vertices(nodeToRemove)

#Rebuild network data. Total capacities connected to each vertice.
finalSumsCon=[]
prod=0
consumed=0
for i in g.vs:
    i["capCur"]=i["cap"]
    sumCon=0
    edges_attached=g.incident(i, mode="ALL")
    i["att"]=edges_attached
    temp=g.es[edges_attached]["cap"]
    prod+=max(0, i["cap"])
    consumed+=min(0, i["cap"])
    for j in range(0, len(temp)):
        temp[j]=0
    i["attCapUsed"]=dict(zip(i["att"], temp))
    for j in edges_attached:
        sumCon=sumCon+g.es[j]["cap"]
    finalSumsCon+=[sumCon]
for i in g.es:
    i["capCur"]=0

#Checking if network even has a chance of delivering electricity to each node
networkCanHandleLoad=1
counter=0
adjuster=0
extraCapacity=np.subtract(finalSumsCon, np.subtract(0, g.vs[:]["cap"]))
for i in extraCapacity:
    if counter>=nodeToRemove:
        adjuster=1
    if i < 0:
        print("Not enough capacity in vertice: ", counter+adjuster, " missing: ", abs(i), " delivered: ", finalSumsCon[counter], " consumes: ", -g.vs[counter]["cap"])
        networkCanHandleLoad=0
    counter+=1

if networkCanHandleLoad==0:
    print("Electricity supply network cannot handle removing node ", nodeToRemove, ". Capacity connected to this node is too small to satisfy the demand after node removed.")
else:
    print("We will now attempt balancing the network after node ", nodeToRemove, " is removed...")
    [g, balanced]=balanceNetwork(g, MAXCHNG)
    avgEdgeBandwidth=np.sum(g.es[:]["cap"])/numEdg
    extraTotalBandwidth=np.sum(g.es[:]["cap"])-np.sum(g.es[:]["capCur"])


    #Network energy data aggregates presented
    print("Num edges: ", len(g.es), "Num vertices: ", len(g.vs))
    print("Net energy value: ", sum)
    print("\tEnergy produced: ", prod)
    print("\tEnergy consumed: ", consumed)
    print("Average edge bandwidth: %.2f" % avgEdgeBandwidth)
    print("Extra bandwidth available in the whole network: ", extraTotalBandwidth)

    #Edges at peak bandwidth
    peakBandwidth=[]
    for i in g.es:
        if i["capCur"]>=0.9*i["cap"]:
            peakBandwidth+=[i.index]
    print("Edges close to or at peakBandwidth: ", peakBandwidth)
    if balanced:
        print("\nSUCCESS!\nRemoval of node ", nodeToRemove, "can be handled by this network.")

print("Check", g.vs[0])
print("Check2", g.es[0])
#Done initial checking.

#displayGraph(g)

print ("Simulation finished!")
