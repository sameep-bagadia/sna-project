import snap

G = snap.LoadEdgeList(snap.PUNGraph, "modified/edges.txt")
print "Nodes = %d, Edges = %d" % (G.GetNodes(), G.GetEdges())

#degree distribution
snap.PlotOutDegDistr(G, "Deg_dist", "Degree Distribution")
print "Average degree = %f" % (2.0 * float(G.GetEdges()) / float(G.GetNodes()))

# clustering coefficient
snap.PlotClustCf(G, "Clust_coeff", "Clustering coefficient")
CfVec = snap.TFltPrV()
Cf = snap.GetClustCf(G, CfVec, -1)
print "Clustering coefficient = %f" % (Cf)

print "Approximate Diameter = %d" % (snap.GetBfsFullDiam(G, 10))
print "Fraction of nodes in largest connected component = %f" % (snap.GetMxWccSz(G))
