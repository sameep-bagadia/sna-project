import snap
import itertools
#keep node1 <= node2 in dictionary

def iter_simrank(G, simrank, C, threshold):
	simrank_new = dict()

	# Calculate the summation part
	for key in simrank.keys():
		node1 = key[0]
		node2 = key[1]
		if (node1 == node2):
			for out1 in G.GetNI(node1).GetOutEdges():
				for out2 in G.GetNI(node2).GetOutEdges():
					if (out1 < out2):
						if (simrank_new.has_key((out1, out2))):
							simrank_new[(out1, out2)] =  simrank_new[(out1, out2)] + simrank[(node1, node2)]
						else:
							simrank_new[(out1, out2)] = simrank[(node1, node2)]
		else:
			for out1i in G.GetNI(node1).GetOutEdges():
				for out2i in G.GetNI(node2).GetOutEdges():
					if (out1i != out2i):
						if (out1i > out2i):
							(out1, out2) = (out2i, out1i)
						else:
							(out1, out2) = (out1i, out2i)
						if (simrank_new.has_key((out1, out2))):
							simrank_new[(out1, out2)] = simrank_new[(out1, out2)] + simrank[(node1, node2)]
						else:
							simrank_new[(out1, out2)] = simrank[(node1, node2)]

	# Calculate score and prune out
	for key in simrank_new.keys():
		node1 = key[0]
		node2 = key[1]
		simrank_new[(node1, node2)] = float(simrank_new[(node1, node2)]) * C / (float(G.GetNI(node1).GetDeg() * G.GetNI(node2).GetDeg()))
		
		if (simrank_new[(node1, node2)]) < threshold:
			del simrank_new[(node1, node2)]

	for node in G.Nodes():
		simrank_new[(node.GetId(), node.GetId())] = 1.0

	return simrank_new
		

def calculate_simrank(G, C, threshold, iter_count):
	simrank = {}
	# Initialize simrank of node with itself as 1
	for node in G.Nodes():
		simrank[(node.GetId(), node.GetId())] = 1.0

	for iter_no in xrange(iter_count):
		print "Starting iteration number : %d" % (iter_no)
		simrank_new = dict()
		simrank_new.clear()
		simrank_new = iter_simrank(G, simrank, C, threshold)
		simrank.clear()
		simrank = simrank_new

	return simrank

def print_simrank(simrank):
	for key in simrank.keys():
		print key, simrank[key]
		#print "simrank(%d, %d) = %f" % (key[0], key[1], simrank[key])

def main():
	filename = raw_input("Enter filename: ")
	G = snap.LoadEdgeList(snap.PUNGraph, filename)
	simrank = calculate_simrank(G, 0.6, 0.01, 5)
	print_simrank(simrank)

main()
