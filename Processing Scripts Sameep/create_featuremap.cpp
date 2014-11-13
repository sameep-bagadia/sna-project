#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <vector>
using namespace std;

int main() {

	//Generate the feature to feature-id mapping. 
	//Feature id is the position of the feature in global features file. 
	//Index starts from 0.
	map<string, int> feat_map;
	FILE* fglobal_feat = fopen("Processed_Data_Rohit/globalFeatureList.globalFeatureList","r");
	if (fglobal_feat == NULL) {printf("Error opening Processed_Data_Rohit/globalFeatureList.globalFeatureList");}
	int i = 0;
	char featurec[200];
	while (fscanf(fglobal_feat, "%s", featurec) != EOF) {
		string feature = featurec;
		feat_map[feature] = i;
		i++;
	}
	fclose(fglobal_feat);

	// Open the file to store feature edge of egonodes only
	FILE* fego_feat_edge = fopen("modified/feat_edges_ego_raw.txt","w");
	if (fego_feat_edge == NULL) {printf("Error opening modified/feat_edges_ego_raw.txt\n");}

	// Open the file to store all feature edges
	FILE* fall_feat_edge = fopen("modified/feat_edges_raw.txt","w");
	if (fall_feat_edge == NULL) {printf("Error opening modified/feat_edges_raw.txt\n");}

	// Open the file containing the list of egonodes
	FILE* fnodelist = fopen("modified/egonodes.txt","r");
	if (fnodelist == NULL) {printf("Error opening modified/egonodes.txt\n");}
	
	char node_id[200];
	int total_files = 973;
	int current_file = 1;
	while (fscanf(fnodelist, "%s", node_id) != EOF) {
		printf("File %d / %d\n", current_file, total_files);

		//opening ego features map file
		char ego_feat_file[200];
		ego_feat_file[0] = '\0';
		strcat(ego_feat_file, "original/");
		strcat(ego_feat_file, node_id);
		strcat(ego_feat_file, ".egofeat");
		FILE* fego_feat = fopen(ego_feat_file, "r");
		if (fego_feat == NULL) {printf("Error opening %s\n", ego_feat_file);}

		//opening cleaned feature list file
		char cleaned_feat_file[200];
		cleaned_feat_file[0] = '\0';
		strcat(cleaned_feat_file, "Processed_Data_Rohit/");
		strcat(cleaned_feat_file, node_id);
		strcat(cleaned_feat_file, ".featnamesclean");
		FILE* fcleaned_feat = fopen(cleaned_feat_file, "r");
		if (fcleaned_feat == NULL) {printf("Error opening %s\n", cleaned_feat_file);}

		//opening features map file of egonetwork of the egonode 
		char all_feat_file[200];
		all_feat_file[0] = '\0';
		strcat(all_feat_file, "original/");
		strcat(all_feat_file, node_id);
		strcat(all_feat_file, ".feat");
		FILE* fall_feat = fopen(all_feat_file, "r");
		if (fall_feat == NULL) {printf("Error opening %s\n", all_feat_file);}

		//Generate a mapping from local feature id to global feature id
		vector<int> local2global;
		char local_featurec[200];
		while (fscanf(fcleaned_feat, "%s", local_featurec) != EOF) {
			fscanf(fcleaned_feat, "%s", local_featurec);
			string local_feature = local_featurec;
			if(feat_map.count(local_feature) > 0) {
				local2global.push_back(feat_map[local_feature]);
			}
			else {
				local2global.push_back(-1);
			}
			
		}
		int local_feature_count = local2global.size();

		//Processing the ego nodes features (egofeat)
		int flag;
		for (int id = 0; id < local_feature_count; id++) {
			fscanf(fego_feat, "%d", &flag);
			if (flag == 1) {
				fprintf(fego_feat_edge, "%s\t%d\n", node_id, local2global[id]);
				fprintf(fall_feat_edge, "%s\t%d\n", node_id, local2global[id]);
			}
		}

		//Processing the features of ego-network (feat)
		int node_id2;
		int flag2;
		while (fscanf(fall_feat, "%d", &node_id2) != EOF) {
			for (int i = 0; i < local_feature_count; i++) {
				fscanf(fall_feat, "%d", &flag2);
				if (flag2 == 1) {
					fprintf(fall_feat_edge, "%d\t%d\n", node_id2, local2global[i]);
				}
			}
		}
		//Close files
		fclose(fego_feat);
		fclose(fcleaned_feat);
		fclose(fall_feat);
		current_file++;
	}
	//Close files
	fclose(fego_feat_edge);
	fclose(fall_feat_edge);
	fclose(fnodelist);
	return 0;
}
