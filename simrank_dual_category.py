def get_categorynumber_category_mapper():
	categorynumber_category_mapper = dict()
	input_file_name = 'feature_list.txt'
	with open(input_file_name) as f:
		line_number = 0
		for line in f:
			line = line[:-1]
			category = line
			categorynumber_category_mapper[line_number] = category
			line_number += 1
	return categorynumber_category_mapper

def get_node(string):
	return int((string.split())[1])
	#return int((str.split(string, ', '))[0])

def get_type_map(filename):
	type_map = dict()
	node_list = map(get_node, open("graphs_dual_categories/" + filename + ".txt", 'r').read().splitlines())
	type_list = map(int, open("dual_category_map/" + filename + "_categoryid.txt", 'r').read().splitlines())
	for i in xrange(len(node_list)):
		type_map[node_list[i]] = type_list[i]
	return type_map

def calculate(category_map, filepath, filename):

	type_map = get_type_map(filename)

	outfile = 'simrank_dual_filtered/' + filename + '_dual_simrank.txt'
	fout = open(outfile, 'w')
	with open(filepath) as f:
		for line	 in f:
			line = line[:-1]
			line_vec =  str.split(line, ', ')
			node1 = int(line_vec[0])
			node2 = int(line_vec[1])
			score = float(line_vec[2])
			if ((node1 >= 1000000000) and (score < 1)):
				if (type_map[node1] != type_map[node2]):
					node1a = node1 - 1000000000
					node2a = node2 - 1000000000
					#print node1a, node2a
					fout.write('%s %s %.10f\n' % (category_map[node1a], category_map[node2a], score))

def main():
	count = 48
	total_files = 258
	category_map = get_categorynumber_category_mapper()
	with open('dual_simrank_list.txt') as f:
		for filename in f:
			filepath = 'simrank_dual/'
			filename = filename[:-1]
			filepath = filepath + filename + '.txtoutput'
			print "Starting %s (%d/%d)" % (filename, count, total_files)
			calculate(category_map, filepath, filename)
			count += 1


main()
