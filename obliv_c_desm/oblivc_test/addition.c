#include<stdio.h>
#include<stdlib.h>
#include<obliv.h>

#include"addition.h"

int setup(int party, int number){
	if(2==2){
		//localhost: 127.0.0.1
		const char *remote_host = "127.0.0.1";
		const char *port = "1234";
		ProtocolDesc pd;
		protocolIO io;

		if(party==1){
			printf("accepting");
			if(protocolAcceptTcp2P(&pd, port)!=0){
				printf("TCP accept failed\n");
				exit(1);
			}
		}
		else{
			printf("connecting");
			if(protocolConnectTcp2P(&pd, remote_host, port)!=0){
				printf("TCP connect failed\n");
				exit(1);
			}
		}

		//Initilization before entering protocol..
		int cp = (party==1 ? 1 : 2);
		setCurrentParty(&pd, cp);
		io.num = number;
		
		execYaoProtocol(&pd, add, &io);
		cleanupProtocol(&pd);

		printf("Result: %d\n", io.sum);

	}

	else{
		fprintf(stderr, "Argument missing (party, number)\n");
		return 1;
	}

	return 0;
}


