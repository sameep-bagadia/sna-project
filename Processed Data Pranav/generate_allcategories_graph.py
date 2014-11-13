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

def read_featureGenreMap():   # MAP from feature_name to set of genres (string representations for all)
	input_file_name = './input_data/featureGenreMap.json'
	featureGenreMap = dict()
	addFileToFeatureSet(featureGenreMap, input_file_name)

	# for key in featureGenreMap:
	# 	for item in featureGenreMap[key]:
	# 		if len(featureGenreMap[key]) >= 1 and len(featureGenreMap[key]) <= 2:
	# 			print key, item
	return featureGenreMap

def get_category_number_mapper():
	category_number_mapper = dict()
	input_file_name = './data_statistics/category_list.txt'
	with open(input_file_name) as f:
		line_number = 0
		for line in f:
			line = line[:-1]
			category = line
			category_number_mapper[category] = line_number
			line_number += 1
	return category_number_mapper


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

def category_checker_for_featurename_allcategories(feature_id_to_name_map, featureGenreMap, feature_id):
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
	return True

def get_categorynumbers_for_featurename(feature_id_to_name_map, featureGenreMap, category_number_mapper, feature_id):  # checks if a feature name belongs to a particular category
	
	#---------------------------------------- Filters on the feature name ----------------------------------------
	min_number_categories_celeb = 1
	max_number_categories_celeb = 1000  # remove all celebs with more number of categories (since the celebs might have a noisy relation to each category)
	
	#--------------------------------------------------------------------------------------------------------------
	# category_checker_for_featurename()   should be executed before this to check if the mapping for the feature to a category actually exists
	feature_name = feature_id_to_name_map[feature_id]
	list_genres = featureGenreMap[feature_name]
	
	category_numbers = []
	for item in list_genres:
		category_numbers.append(category_number_mapper[item])
	return category_numbers


def get_category_list():
	input_file_name = './data_statistics/category_list.txt'
	list_categories = []
	with open(input_file_name) as f:
		for line in f:
			line = line[:-1]
			list_categories.append(line)
	return list_categories

def main():

	#-----------------------------------------Get the Mappings!--------------------------------------------------
	category_number_mapper = get_category_number_mapper()
	featureGenreMap = read_featureGenreMap()
	feature_id_to_name_map = feature_id_feature_name()
	list_categories = get_category_list()   # What categories do you want to generate the graphs for?
	#--------------------------------------------------------------------------------------------------------------
	#----------------------------------- Reading node to feature edge list ------------------------------------------
	input_file_name = './input_data/feat_edges.txt'
	start_celeb_id = pow(10,9)

	output_file_name = './output_data/node_categorynode_graph_allcategories.txt'
	print 'Writing to file: ',output_file_name
	f_output = open(output_file_name, 'w')


	edge_map = dict()
	no_nodes_done = 0
	with open(input_file_name) as f:
		for line in f:
			no_nodes_done += 1
			line = line[:-1]
			line_vec =  str.split(line, '\t')
			node_id = long(line_vec[0])
			celeb_id = long(line_vec[1])
			if not category_checker_for_featurename_allcategories(feature_id_to_name_map, featureGenreMap, celeb_id):
				continue
			category_numbers = get_categorynumbers_for_featurename(feature_id_to_name_map, featureGenreMap, category_number_mapper, celeb_id)
			for category_id in category_numbers:
				edge_map[(category_id, node_id)] = 1

	for edge in edge_map:
		output_string = '%ld\t%ld\n'%(start_celeb_id + edge[0], edge[1])
		f_output.write(output_string)

		


if __name__ == '__main__':
	main()