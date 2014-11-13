import snap
from math import *
import random
import numpy as np
from bisect import bisect
import matplotlib.pyplot as plt
import json
from pprint import pprint

def get_categorynumber_category_mapper():
	categorynumber_category_mapper = dict()
	input_file_name = './data_statistics/category_list.txt'
	with open(input_file_name) as f:
		line_number = 0
		for line in f:
			line = line[:-1]
			category = line
			categorynumber_category_mapper[line_number] = category
			line_number += 1
	return categorynumber_category_mapper

def plot_graph_stats(G, IsDir):
	CfVec = snap.TFltPrV()
	Cf = snap.GetClustCf(G, CfVec, -1)
	print "Average Clustering Coefficient for Graph: %f" % (Cf)
	NTestNodes = 10
	EffDiam1 = snap.GetBfsEffDiam(G, NTestNodes, IsDir)
	print 'Diamter for Graph= %d'%(EffDiam1)
	# snap.PlotInDegDistr(G, "G", "Degree Distribution", False, False)
	# snap.PlotOutDegDistr(G, "G", "Degree Distribution", False, False)
	MxScc = snap.GetMxScc(G)
	print 'SCC: Number of nodes = %d, edges = %d'%(MxScc.GetNodes(), MxScc.GetEdges())
	print 'Fractional Size SCC of Graph: %f' %(snap.GetMxSccSz(G))

	no_users = 0
	no_categories = 0
	for nit in G.Nodes():
		cur_node = nit.GetId()
		if cur_node < pow(10,9):
			no_users += 1
		else:
			no_categories += 1

	print 'Number of users = %d, categories = %d'%(no_users, no_categories)


def get_graph_measures(G, categorynumber_category_mapper):

	# Nodes = snap.TIntFltH()
	# Edges = snap.TIntPrFltH()
	# snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
	PRankH = snap.TIntFltH()
	snap.GetPageRank(G, PRankH)
	# NIdHubH = snap.TIntFltH()
	# NIdAuthH = snap.TIntFltH()
	# snap.GetHits(Graph, NIdHubH, NIdAuthH)

	for nit in G.Nodes():
		node = nit.GetId()
		if node >= pow(10,9):  # i.e. a category node
			FarCentr = snap.GetFarnessCentr(G, nit.GetId())
			DegCentr = snap.GetDegreeCentr(G, nit.GetId())
			Necc = snap.GetNodeEcc(G, nit.GetId(), True)

			# print "%d, %f, %f, %f\n"%(node, FarCentr, DegCentr, Necc)
			# print "Betweenness centrality: %f" %(Nodes[node])
	output_file_name = './graphs/category_scores/allcategorygraph_pageranks.txt'
	f_output = open(output_file_name, 'w')
	for item in PRankH:
		if item >= pow(10,9):
			s = '%d, %f\n'%(categorynumber_category_mapper[item-pow(10,9)], PRankH[item])
			f_output.write(s)



def main():
	IsDir = False
	if IsDir:
		G = snap.LoadEdgeList(snap.PNGraph, "./graphs/node_categorynode_graph_allcategories.txt", 0, 1)
		# G = snap.LoadEdgeList(snap.PNGraph, "./output_data/node_categorynode_graph_240categories.txt", 0, 1)
	else:
		G = snap.LoadEdgeList(snap.PUNGraph, "./graphs/node_categorynode_graph_allcategories.txt", 0, 1)
		# G = snap.LoadEdgeList(snap.PUNGraph, "./output_data/node_categorynode_graph_240categories.txt", 0, 1)
	number_nodes = G.GetNodes()
	number_edges = G.GetEdges()

	print 'Number of nodes = %d, edges = %d'%(number_nodes, number_edges)

	categorynumber_category_mapper = get_categorynumber_category_mapper()
	# plot_graph_stats(G, IsDir)
	get_graph_measures(G, categorynumber_category_mapper)


if __name__ == '__main__':
	main()
