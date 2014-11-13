#include <iostream>
#include <fstream>
using namespace std;

int main() {
	FILE* fnodelist = fopen("modified/egonodes.txt","r");
	if (fnodelist == NULL) {printf("Error opening modified/egonodes_list.txt\n");}
	FILE* fedgelist = fopen("modified/raw_edges.txt", "w");
	if (fedgelist == NULL) {printf("Error opening modified/raw_edges.txt\n");}
	char node_id[200];
	int total_files = 973;
	int current_file = 1;
	while (fscanf(fnodelist, "%s", node_id) != EOF) {
		printf("File %d / %d\n", current_file, total_files);
		char node_edge_file[200];
		node_edge_file[0] = '\0';
		strcat(node_edge_file, "original/");
		strcat(node_edge_file, node_id);
		strcat(node_edge_file, ".edges");
		FILE* ftriads = fopen(node_edge_file, "r");
		if (ftriads == NULL) {printf("Error opening %s\n", node_edge_file);}
		int node1, node2;
		while (fscanf(ftriads, "%d %d", &node1, &node2) != EOF) {
			fprintf(fedgelist, "%s\t%d\n", node_id, node1);
			fprintf(fedgelist, "%s\t%d\n", node_id, node2);
			fprintf(fedgelist, "%d\t%d\n", node1, node2);
		}
		fclose(ftriads);
		current_file++;
	}
	printf("here\n");
	fclose(fnodelist);
	fclose(fedgelist);
	return 0;
}
	
