#include<stdio.h>
#include<stdlib.h>
#include<obliv.h>

#include"addition.h"

int main(int argc, char *argv[]){
	if(argc==3){
		//localhost: 127.0.0.1
		const char *remote_host = "127.0.0.1";
		const char *port = "1234";
		ProtocolDesc pd;
		protocolIO io;

		if(argv[1][0]=='1'){
			if(protocolAcceptTcp2P(&pd, port)!=0){
				printf("TCP accept failed");
				exit(1);
			}
		}
		else{
			if(protocolConnectTcp2P(&pd, remote_host, port)!=0){
				printf("TCP connect failed");
				exit(1);
			}
		}

		//Initilization before entering protocoll..
		int cp = (argv[1][0]=='1' ? 1 : 2);
		setCurrentParty(&pd, cp);
		io.num = atoi(argv[2]);
		
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


