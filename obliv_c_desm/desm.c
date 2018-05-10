#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include <time.h>

#include<obliv.h>

#include"desm.h"

//Compute euclidean norm locally (called in oc-File)
float euclid(float *vec, int n){

	//Initilize obliv variables
	float norm;
	float result;
	//Initilize loop-helper
	int i;

	norm = 0;

	for(i = 0; i < n; i = i+1){
		norm = norm + vec[i]*vec[i];
	}

	return sqrt(norm);
}


// Allocate memory for dynamics array in struct
void create_array(protocolIO *io){

	float *arrayd = malloc(sizeof(float) * 5);
	io->scores = arrayd;
	
	float **arraydd = malloc(io->m * sizeof(float*));
	for(int i=0; i<io->m; i++){
		arraydd[i] = malloc(io->n * sizeof(float));
	}
	io->vecs = arraydd;
}

struct sorted_rank { float value; int index; };


int compare_scores(const void *a, const void *b){
	struct sorted_rank *da = (struct sorted_rank *) a;
	struct sorted_rank *db = (struct sorted_rank *) b;

	if(da->value > db->value) return -1;
	else if (da->value < db->value) return 1;
	else return 0;
}


// Setup for each party: Arguments are the party, the document/word vectors, 
// amount of Documents or Query-Words
int * setup(int party, float vecs[][200], int amount, int n, int *scores, int topN){
	if(party==1 | party==2){

		clock_t tGlob;
		clock_t tLoc;
		double time_taken;

		tGlob = clock();
		tLoc = clock();

		//localhost: 127.0.0.1
		const char *remote_host = "127.0.0.1";
		const char *port = "1234";
		ProtocolDesc pd;
		protocolIO io;  // = malloc(sizeof(io) + amount*sizeof(*io->scores));// + amount*n*sizeof(*io->vecs));

		io.m = amount;
		io.n = n;

		create_array(&io);

		if(party==1){
			if(protocolAcceptTcp2P(&pd, port)!=0){
				printf("TCP accept failed\n");
				exit(1);
			}
		}
		else{
			if(protocolConnectTcp2P(&pd, remote_host, port)!=0){
				printf("TCP connect failed\n");
				exit(1);
			}
		}

		//Initilization before entering protocol
		int cp = (party==1 ? 1 : 2);
		setCurrentParty(&pd, cp);

		//Save the Input-vectors and the count to the struct shared with oblivc-Code
		for (int i = 0; i < amount; i++){
			for (int j = 0; j < n; j++){
				io.vecs[i][j] = vecs[i][j];
			}
		}
		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] yao protocol setup: %f seconds --\n", time_taken);

		tLoc = clock();
		//Start secure computation code here
		execYaoProtocol(&pd, desm, &io);

		//clean project
		cleanupProtocol(&pd);

		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] yao protocol terminated: %f seconds --\n", time_taken);

		//Sort and return the scores to python-reachable variable for party 2 (who provided the query)
		if(party==2){

			tLoc = clock();

			struct sorted_rank *ranking = malloc(sizeof(*ranking) * io.count_doc);

			for(int i = 0; i < io.count_doc; i++){
				ranking[i].value = io.scores[i];
				ranking[i].index = i;
			}

			qsort(ranking, io.count_doc, sizeof(ranking[0]), compare_scores);
			tLoc = clock() - tLoc;
			time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
			printf("-- [C] sort rankings: %f seconds --\n", time_taken);


			if(io.count_doc < topN){
				for (int i = 0; i < io.count_doc; i++){
					printf("\nScore: %f\n", ranking[i].value);
					scores[i] = ranking[i].index;
				}
			}
			else{
				for (int i = 0; i < topN; i++){
					printf("\nScore: %f\n", ranking[i].value);
					scores[i] = ranking[i].index;
				}
			}
		}

		printf("\nDone!\n");

		tGlob = clock() - tGlob;
		time_taken = ((double) tGlob) / CLOCKS_PER_SEC;
		printf("-- [C] Whole runtime: %f seconds --\n", time_taken);

		return 0;
	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}
	
}
