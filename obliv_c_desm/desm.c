#include<stdio.h>
#include<stdlib.h>
#include<math.h>

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

// Setup for each party: Arguments are the party, the document/word vectors, 
// amount of Documents or Query-Words
int * setup(int party, float vecs[][200], int amount, int n, float scores[]){

	if(party==1 | party==2){

		//localhost: 127.0.0.1
		const char *remote_host = "127.0.0.1";
		const char *port = "1234";
		ProtocolDesc pd;
		protocolIO io;

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

		io.m = amount;
		io.n = n;

		//Start secure computation code here
		execYaoProtocol(&pd, desm, &io);

		//clean project
		cleanupProtocol(&pd);

		//Return the scores to python-reachable variable for party 2 (who provided the query)
		if(party==2){
			for (int i = 0; i < 5; i++){
				scores[i] = io.scores[i];
			}
		}

		printf("\nDone!\n");

		return 0;

	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}
	
}
