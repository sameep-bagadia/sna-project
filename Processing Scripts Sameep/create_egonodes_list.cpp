#include <iostream>

using namespace std;

int main() {
	char filename[200];
	while (scanf("%s", filename) != EOF) {
		for (unsigned int i = 0; i < 200; i += 1){
			if (filename[i] == '.') {
				filename[i] = '\0';
				break;
			}
		}
		printf("%s\n", filename);
		for (unsigned int i = 0; i < 4; i += 1)
		{
			scanf("%s", filename);
		}
	}
	return 0;
}
	
