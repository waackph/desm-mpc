typedef struct{
	float vecs[5][200];
	int amount;
	float scores[5];
} protocolIO;

void desm(void* args);

float * setup(int party, float vecs[][200], int amount);
