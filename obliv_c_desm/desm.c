#include<stdio.h>
#include<stdlib.h>
#include<obliv.h>

#include"desm.h"

float * setup(int party, float vecs[][200], int amount){
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

		//Initilization before entering protocol..
		int cp = (party==1 ? 1 : 2);
		setCurrentParty(&pd, cp);

		//memcpy(io->vecs, vecs, sizeof vecs);
		io.vecs = vecs;
		io.amount = amount;
		
		execYaoProtocol(&pd, desm, &io);
		cleanupProtocol(&pd);

		printf("Done!\n");

		return io.scores;

	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}
	
}
