#include<stdio.h>
#include<stdlib.h>
#include<obliv.h>

#include"desm.h"

// Setup for each party: Arguments are the party, the document/word vectors, 
// amount of Documents or Query-Words
int * setup(int party, float vecs[][200], int amount, float scores[]){
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

		// T *p = malloc(sizeof(*p) * N) will allocate N instances of T
		// T *p[10] = malloc(sizeof(*p) * N) will allocate N instances of T[200]
		//float (*temp)[200] = malloc(sizeof(*temp) * amount);
		for (int i = 0; i < amount; i++){
			for (int j = 0; j < 200; j++){
				io.vecs[i][j] = vecs[i][j];
			}
		}

		io.m = amount;
		io.n = 200;
		//io.vecs = temp;

		printf("\n\n%f\n\n", io.vecs[0][7]);
		//printf("\n\n%f\n\n", temp[0][0]);
		//printf("\n\n%f\n\n", tst);

		//Start secure computation code here
		execYaoProtocol(&pd, desm, &io);

		//clean project
		cleanupProtocol(&pd);
		printf("Done!\n");

		//Return the scores to python-reachable variable for party 2 (who provided the query)
		if(party==2){
			for (int i = 0; i < 5; i++){
				scores[i] = io.scores[i];
			}
		}
		return 0;

	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}
	
}