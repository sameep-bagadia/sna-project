edge_list = open('modified/feat_edges_ego_raw.txt', 'r').read().splitlines()

# remove duplicates
mydict = {}
for edge in edge_list:
	sepedge = edge.split()
	mydict[(sepedge[0], sepedge[1])] = 1

#store the output

fout = open('modified/feat_edges_ego.txt', 'w')
for key in mydict.keys():
	#print key
	if(key[1] != '-1'):
		fout.write(key[0])
		fout.write("\t")
		fout.write(key[1])
		fout.write("\n")
