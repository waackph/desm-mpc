#~/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/obliv-c/bin/oblivcc addition.c addition.h addition.oc -I addition -c -o addition.o

#~/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/obliv-c/bin/oblivcc addition_old.c addition.h addition.oc -o addition

~/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/obliv-c/bin/oblivcc addition.c addition.h addition.oc -I . -shared -fPIC -o libaddition.so

