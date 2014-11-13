import snap

G = snap.LoadEdgeList(snap.PUNGraph, "modified/raw_edges.txt")
snap.SaveEdgeList(G, 'modified/edges.txt')

fnodes = open('modified/nodes.txt', 'w')
NodeI = G.BegNI()
while(NodeI != G.EndNI()):
	fnodes.write(str(NodeI.GetId()))
	fnodes.write("\n")
	NodeI.Next()
