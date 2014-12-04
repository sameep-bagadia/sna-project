import snap
from multiprocessing import Process
from os import listdir, getcwd
from os.path import isfile, join
import time
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

def print_simrank(simrank, filename):
    output_file = filename + "output"
    f_output = open(output_file, 'w')
    for key in simrank.keys():
        s = '%d, %d, %f\n'%(key[0], key[1], simrank[key])
        f_output.write(s)
    f_output.close()

		#print "simrank(%d, %d) = %f" % (key[0], key[1], simrank[key])

def getNumAlive(processList):
    numAlive = 0
    for i in range(len(processList)):
        if processList[i].is_alive():
            numAlive = numAlive + 1
    return numAlive

def main(filename):
	G = snap.LoadEdgeList(snap.PUNGraph, filename)
	simrank = calculate_simrank(G, 0.6, 0.01, 5)
	print_simrank(simrank, filename)


if __name__ == "__main__":
    currdir = getcwd()
    foldername = "graphs_by_category"
    directory = currdir+"/"+foldername+"/"

    onlyfiles = [f for f in listdir(directory) if isfile(join(directory,f)) ]

    processList = list()

    for i in range(len(onlyfiles)):
        print directory+onlyfiles[i]
        processList.append(Process(target=main, args = (directory+onlyfiles[i],)))

    numAlive = getNumAlive(processList)
    maxAlive = 10

    for i in range(len(processList)):
        numAlive = getNumAlive(processList)
        while numAlive > maxAlive:
            time.sleep(5)
            numAlive = getNumAlive(processList)
        print "Number of processes alive : ", numAlive
        processList[i].start()

