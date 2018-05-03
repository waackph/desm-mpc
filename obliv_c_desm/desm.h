#include<stddef.h>

typedef struct{
	size_t m;
	size_t n;
	float scores[5];
	float vecs[5][200];
} protocolIO;

void desm(void* args);

int * setup(int party, float vecs[][200], int amount, int n, float scores[]);

float euclid(float *vec, int n);
