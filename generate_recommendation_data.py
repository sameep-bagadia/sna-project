import snap


def main():
	# Initialize the datastructure data : (dict<egonodeid, dict<nodeid, list<feature>>>)
	print "Initializing datastructures"
	user_graph = snap.LoadEdgeList(snap.PUNGraph, "modified/edges.txt")
	egonodes_list = open('modified/egonodes.txt', 'r').read().splitlines()
	data = dict()
	total_egonodes = len(egonodes_list)
	egonodes_count = 0
	for egonode_str in egonodes_list:
		egonodes_count += 1
		print "Initializing datastructures for egonode : %s (%d / %d)" % (egonode_str, egonodes_count, total_egonodes)
		
		egonode = int(egonode_str)
		data[egonode] = dict()
		for NI in user_graph.Nodes():
			nodeid = NI.GetId()
			if (nodeid != egonode):
				data[egonode][nodeid] = list()

	print "Datastructures Initialized"
	print "Processing each interest:"
		
	# For each interest simrank file, store the simrank values in dict<(node1, node2), score>
	interest_list = open('simrank_list.txt', 'r').read().splitlines()
	total_interests = len(interest_list)
	interest_count = 0
	for interest in interest_list:
		interest_count += 1
		print "Processing interest : %s (%d / %d)" % (interest, interest_count, total_interests)
		simrank = dict()
		simrank_filepath = "simrank_data/" + interest + ".txtoutput"
		with open(simrank_filepath) as f:
			for line in f:
				line = line[:-1]
				line_vec =  str.split(line, ', ')
				node1 = int(line_vec[0])
				node2 = int(line_vec[1])
				score = float(line_vec[2])
				simrank[(node1, node2)] = score
				
		# For each egonode, calculate Q2i, add a column to X[egonode]
		for egonode_str in egonodes_list:
			egonode = int(egonode_str)
			Q2i = 0.0
			count = 0
			for nodeid in data[egonode].keys():
				count += 1
				if (simrank.has_key((min(egonode, nodeid), max(egonode, nodeid)))):
					Q2i += simrank[(min(egonode, nodeid), max(egonode, nodeid))]
			Q2i = Q2i / float(count)

			for nodeid in data[egonode].keys():
				if (simrank.has_key((min(egonode, nodeid), max(egonode, nodeid)))):
					#print "here"
					data[egonode][nodeid].append(simrank[(min(egonode, nodeid), max(egonode, nodeid))] / Q2i)
				else:
					data[egonode][nodeid].append(0.0)

	print "Processing done"
	print "Storing output"
	# store the values in different file for each egonode, also store the labels

	total_egonodes = len(egonodes_list)
	egonodes_count = 0
	for egonode_str in egonodes_list:
		egonodes_count += 1
		print "Storing output for egonode : %s (%d / %d)" % (egonode_str, egonodes_count, total_egonodes)
	
		egonode = int(egonode_str)
	
		features_file = "recommendation_data/features/" + egonode_str + "_X.txt"
		labels_file = "recommendation_data/labels/" + egonode_str + "_y.txt"
		node_sequence_file = "recommendation_data/node_sequence/" + egonode_str + "_node_sequence.txt"
		features_out = open(features_file, 'w')
		labels_out = open(labels_file, 'w')
		node_sequence_out = open(node_sequence_file, 'w')

		for nodeid in data[egonode].keys():
			for feature in data[egonode][nodeid]:
				features_out.write("%.10f " % (feature))
			features_out.write("\n")

			if (user_graph.IsEdge(egonode, nodeid)):
				labels_out.write("1\n")
			else:
				labels_out.write("0\n")

			node_sequence_out.write("%d\n" % (nodeid))
	

main()
