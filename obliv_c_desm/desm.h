#include<stddef.h>

typedef struct{
	size_t m;
	size_t n;
	size_t count_doc;
	float *scores;
	float **vecs;
} protocolIO;

void desm(void* args);

int * setup(int party, float vecs[][200], int amount, int n, int *scores, int topN);

float euclid(float *vec, int n);

void create_array(protocolIO *io);

int compare_floats(const void *a, const void *b);