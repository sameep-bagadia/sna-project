__author__ = 'pranavj'

import snap
from math import *
import random
import numpy as np
from bisect import bisect
import matplotlib.pyplot as plt
import json
from pprint import pprint


# 2 filters on our data:-
# 1) Filter on categories to be considered for generating the graphs (check categories_manually_pruned.txt)
# 2) Filter on features, those features belonging to too many categories should be pruned out?

def addFileToFeatureSet(featureGenreMap, filename):
    with open(filename) as f:
        for line in f:
            featureGenreMap.update(json.loads(line))

def read_featureGenreMap():   # MAP from feature_name to set of genres
	input_file_name = './input_data/featureGenreMap.json'
	featureGenreMap = dict()
	addFileToFeatureSet(featureGenreMap, input_file_name)

	# for key in featureGenreMap:
	# 	for item in featureGenreMap[key]:
	# 		if len(featureGenreMap[key]) >= 1 and len(featureGenreMap[key]) <= 2 and key == '@Hotwire' and item == 'Travel':
	# 			print key, item

	return featureGenreMap

def feature_id_feature_name():
	feature_id_to_name_map = dict()
	input_file_name = './input_data/globalFeatureList.globalFeatureList'

	line_number = 0   # 0 indexing
	with open(input_file_name) as f:
		for line in f:
			line = line[:-1]  # removing the newline character
			feature_id_to_name_map[line_number] = line
			line_number += 1
	return feature_id_to_name_map

def category_checker_for_featurename(feature_id_to_name_map, featureGenreMap, category, feature_id):  # checks if a feature name belongs to a particular category
	
	#---------------------------------------- Filters on the feature name ----------------------------------------
	min_number_categories_celeb = 1
	max_number_categories_celeb = 1000  # remove all celebs with more number of categories (since the celebs might have a noisy relation to each category)
	
	#--------------------------------------------------------------------------------------------------------------
	if not feature_id in feature_id_to_name_map:
		print 'Mapping for feature id %d does not exist'%(feature_id)
		exit(0)
		return False

	feature_name = feature_id_to_name_map[feature_id]
	if not feature_name in featureGenreMap:
		print 'Feature %s does not exist in the featureGenreMap'%(feature_name)
		exit(0)
		return False

	list_genres = featureGenreMap[feature_name]

	if len(list_genres) < min_number_categories_celeb or len(list_genres) > max_number_categories_celeb:
		return False  # i.e. don't use this feature since it might be noisy

	for item in list_genres:
		# print item, category
		if item == category:
			return True
	return False

def get_category_list():
	input_file_name = './input_data/category_pruned.txt'
	list_categories = []
	with open(input_file_name) as f:
		for line in f:
			line = line[:-1]
			list_categories.append(line)
	return list_categories

def main():
	
	#-----------------------------------------Get the Mappings!--------------------------------------------------
	featureGenreMap = read_featureGenreMap()
	feature_id_to_name_map = feature_id_feature_name()
	list_categories = get_category_list()   # What categories do you want to generate the graphs for?
	#--------------------------------------------------------------------------------------------------------------

	#----------------------------------- Reading node to feature edge list ------------------------------------------
	input_file_name = './input_data/feat_edges.txt'
	start_celeb_id = pow(10,9)
	# category = 'Poetry'

	for i in range(0, len(list_categories)):
		category = list_categories[i]
		output_file_name = './output_data/'+category+'.txt'
		print 'Writing to file: ',output_file_name
		f_output = open(output_file_name, 'w')

		with open(input_file_name) as f:
			# min, max node_id = 12 568770231
			for line in f:
				line = line[:-1]
				line_vec =  str.split(line, '\t')
				node_id = long(line_vec[0])
				celeb_id = long(line_vec[1])
				if category_checker_for_featurename(feature_id_to_name_map, featureGenreMap, category, celeb_id):
					output_string = '%ld\t%ld\n'%(node_id, celeb_id+start_celeb_id)
					f_output.write(output_string)

		f_output.close()


		


if __name__ == '__main__':
	main()