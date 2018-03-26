#include <stdio.h>

int main(){
	float q[3] = {1.0,2.0,3.0};
	int n = sizeof(q);
	printf("%lu\n", n/sizeof(float));
	return 0;
}
