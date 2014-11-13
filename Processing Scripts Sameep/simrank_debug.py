import snap
import itertools
#keep node1 <= node2 in dictionary

def iter_simrank_old(G, simrank, C, threshold):
	for nodei1 in G.Nodes():
		for nodei2 in G.Nodes():
			node1 = nodei1.GetId()
			node2 = nodei2.GetId()
			if (node1 < node2):
				score = 0;
				Nbr1 = nodei1.GetOutEdges()
				Nbr2 = nodei2.GetOutEdges()
				#if ((len(Nbr1) > 0) and (len(Nbr2) > 0)):
				score = 0.0;
				den = 0
				for in1 in Nbr1:
					for in2 in Nbr2:
						den = den + 1
						if (in1 > in2):
							(in1, in2) = (in2, in1)
						if (simrank.has_key((in1, in2))):
							score = score + simrank[(in1, in2)]
				if (score > 0):
					score = (score * C) / (float(den))
				if (score > threshold):
					simrank[(node1, node2)] = score
	return simrank

def iter_simrank(G, simrank, C, threshold):
	simrank_new = dict()

	#Print keys of dictionary
	print "KEYS!"
	print simrank.keys()
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
							if((out1, out2) == (3291841, 17852343)):
								print "simrank_new = %f, inr = %f, node1 = %d, node2 = %d" % (simrank_new[(out1, out2)], simrank[(node1, node2)], node1, node2)
						else:
							simrank_new[(out1, out2)] = simrank[(node1, node2)]
							if((out1, out2) == (3291841, 17852343)):
								print "simrank_new = %f, inr = %f, node1 = %d, node2 = %d" % (simrank_new[(out1, out2)], simrank[(node1, node2)], node1, node2)
		else:
			for out1 in G.GetNI(node1).GetOutEdges():
				for out2 in G.GetNI(node2).GetOutEdges():
					if (out1 != out2):
						if (out1 > out2):
							(out1, out2) = (out2, out1)
						if (simrank_new.has_key((out1, out2))):
							simrank_new[(out1, out2)] =  simrank_new[(out1, out2)] + simrank[(node1, node2)]
							if((out1, out2) == (3291841, 17852343)):
								print "simrank_new = %f, inr = %f, node1 = %d, node2 = %d" % (simrank_new[(out1, out2)], simrank[(node1, node2)], node1, node2)
						else:
							simrank_new[(out1, out2)] = simrank[(node1, node2)]
							if((out1, out2) == (3291841, 17852343)):
								print "simrank_new = %f, inr = %f, node1 = %d, node2 = %d" % (simrank_new[(out1, out2)], simrank[(node1, node2)], node1, node2)

	# Calculate score and prune out
	for key in simrank_new.keys():
		node1 = key[0]
		node2 = key[1]
		if((node1, node2) == (3291841, 17852343)):
			print "simrank = %f, deg1 = %d, deg2 = %d" % (simrank_new[(node1, node2)], G.GetNI(node1).GetDeg() , G.GetNI(node2).GetDeg())
		simrank_new[(node1, node2)] = float(simrank_new[(node1, node2)]) * C / (float(G.GetNI(node1).GetDeg() * G.GetNI(node2).GetDeg()))
		if((node1, node2) == (3291841, 17852343)):
			print "updated simrank = %f, deg1 = %d, deg2 = %d" % (simrank_new[(node1, node2)], G.GetNI(node1).GetDeg() , G.GetNI(node2).GetDeg())
		
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
		print "Starting iteration no %d" % (iter_no)
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
