#include<stdio.h>
#include<stdlib.h>
#include<obliv.h>

#include"desm.h"

// Setup for each party: Arguments are the party, the document/word vectors, 
// amount of Documents or Query-Words
float * setup(int party, float vecs[][200], int amount, float scores[]){
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
		//NOT WORKING YET! HOW TO CORRECTLY SAVE ARRAYS IN STRUCT?
		//memcpy(io->vecs, vecs, sizeof vecs);
		//io.vecs = vecs;
		//io.amount = amount;
		//float *temp[200] = malloc(sizeof(float[amount][200]));
		//assign values to the allocated array...
		/*for (int i = 0; i < amount; i++){
			for (int j = 0; j < 200; j++){
				temp[i][j] = vecs[i][j];
			}
		}*/
		float (*temp)[] = vecs;
		io.m = amount;
		io.n = 200;
		io.array = temp;

		//Start secure computation code here
		execYaoProtocol(&pd, desm, &io);

		//clean project
		cleanupProtocol(&pd);
		printf("Done!\n");

		//Return the scores to python-reachable variable for party 2 (who provided the query)
		if(party==2){
			scores = io.scores;
		}
		return 0;

	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}
	
}
