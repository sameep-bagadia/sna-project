__author__ = 'pranavj'

import snap
from math import *
import random
import numpy as np
from bisect import bisect
import matplotlib.pyplot as plt
import json
from pprint import pprint

# creates a list of categories which can be manually fixed for considering only 'good categories'

def main():
	json_data=open('./input_data/genreFeatureMap.json')
	data = json.load(json_data)
	output_file_name = './data_statistics/category_pruned.txt'
	#--------------------------- Process data ---------------------------
	f_output = open(output_file_name, 'w')
	for key in data:
		if len(data[key]) > 50:   # i.e. the category must have atleast 50 celebs associated
			# print key #, len(data[key])
			f_output.write(key+'\n')
		
	json_data.close()



def build_categ_info_file():
	input_file1 = './data_statistics/category_graphsize.txt'
	input_file2 = './data_statistics/category_to_numberofcelebs.txt'

	output_file_name = './data_statistics/category_info.txt'
	f_output = open(output_file_name, 'w')

	#--------------------------- Read file 1 containing size of each graph ---------------------------
	A1 = dict()
	with open(input_file1) as f:
		for line in f:
			line = line[:-1]
			line_vec =  str.split(line, ', ')
			category_name = line_vec[0]
			number_edges = long(line_vec[1])
			A1[category_name] = number_edges
	#--------------------------------------------------------------------------------------------------

	#--------------------------- Read file2 (number_celebs) and write to file ---------------------------
	with open(input_file2) as f:
		for line in f:
			line = line[:-1]
			line_vec =  str.split(line, ', ')
			category_name = line_vec[0]
			number_celebs = long(line_vec[1])
			output_string = '%s %ld %ld\n'%(category_name, number_celebs, A1[category_name])
			f_output.write(output_string)
	#--------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	# main()
	build_categ_info_file()


