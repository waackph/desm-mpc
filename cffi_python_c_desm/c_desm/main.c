#include <stdio.h>
#include "desm.h"

int main(){
	//initilize output
	float score;
	//initilize test arrays
	float q[][3] = {1.0,2.0,3.0};
	float d[3] = {1.0,2.0,3.0};
	//initilize size of the arrays
	int amountq = sizeof(q) / sizeof(q[0]);
	int n = sizeof(q[0]) / sizeof(q[0][0]);
	score = desm(q, d, n, amountq);
	printf("Score: %f\n", score);
	return 0;
}
