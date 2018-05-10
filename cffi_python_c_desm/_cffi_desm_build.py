from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_cffi_desm",
r""" 
	#include <stdio.h>
	#include <math.h>
	#include <stdlib.h>
	#include <time.h>

	float euclid(float vec[200], int n){
		float norm = 0;
		int i = 0;
		//int n = sizeof(vec)/sizeof(float);
		for(i = 0; i < n; i = i+1){
			norm = norm + vec[i]*vec[i];
		}

		return sqrt(norm);
	}

	float dotprod(float vec1[200], float vec2[200], int n){
		float sum = 0;
		int i = 0;
		//int n = sizeof(vec1)/sizeof(float);
		for(i = 0; i < n; i = i+1){
			//printf("%d\n%f\n%f\n\n", i, vec1[i], vec2[i]);
			sum = sum + vec1[i]*vec2[i];
		}
		return sum;
	}

	float computeCosine(float query[200], float doc[200], int n, float normQuery, float normDoc){
		float dotDoc = dotprod(query, doc, n);
		//printf("%f\n%f\n%f\n", dotDoc, normDoc, normQuery);
		return dotDoc / normQuery * normDoc;
	}

	float desm(float Q[][200], float D[200], int n, int Qn, float normQuerys[], float normDoc){
		//int Qn = sizeof(Q)/sizeof(float);
		int i;
		float newCosine;
		float cosine = 0.0;
		//printf("%d\n", n);
		//printf("%d\n", Qn);
		for(i = 0; i < Qn; i = i+1){
			newCosine = computeCosine(Q[i], D, n, normQuerys[i], normDoc);
			cosine = cosine + newCosine;
		}
		return cosine/Qn;
	}


	struct sorted_rank { float value; int index; };


	int compare_scores(const void *a, const void *b){
		struct sorted_rank *da = (struct sorted_rank *) a;
		struct sorted_rank *db = (struct sorted_rank *) b;

		if(da->value > db->value) return -1;
		else if (da->value < db->value) return 1;
		else return 0;
	}
	

	//args: queries as word-vectors, documents as word-vectors, len(word-vec), amount queries, amount Docs
	int * scores(float Q[][200], float Docs[][200], int n, int Qn, int Dn, int score[], int topN){

		clock_t tGlob;
		clock_t tLoc;
		double time_taken;

		tGlob = clock();

		printf("Allocating Memory..\n");

		//Compute ranking
		int i;

		float normQuerys[Qn];
		float normDocs[Dn];
		float rank[Dn];

		printf("Computing Scores..\n");

		tLoc = clock();
		for(i=0; i<Qn; i++){
			normQuerys[i] = euclid(Q[i], n);
		}
		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] compute Query norms: %f seconds --\n", time_taken);

		tLoc = clock();
		for(i=0; i<Dn; i++){
			normDocs[i] = euclid(Docs[i], n);
		}
		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] compute Doc norms: %f seconds --\n", time_taken);

		tLoc = clock();
		for(i=0; i<Dn; i++){
			rank[i] = desm(Q, Docs[i], n, Qn, normQuerys, normDocs[i]);
		}
		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] compute Rankings: %f seconds --\n", time_taken);

		printf("Sorting ranks..\n");

		tLoc = clock();

		//Sort ranking
		struct sorted_rank *ranking = malloc(sizeof(*ranking) * Dn);

		for(i = 0; i < Dn; i++){
			ranking[i].value = rank[i];
			ranking[i].index = i;
		}

		qsort(ranking, Dn, sizeof(ranking[0]), compare_scores);
		tLoc = clock() - tLoc;
		time_taken = ((double) tLoc) / CLOCKS_PER_SEC;
		printf("-- [C] sort rankings: %f seconds --\n", time_taken);

		if(Dn < topN){
			for (i = 0; i < Dn; i++){
				printf("\nScore: %f\n", ranking[i].value);
				score[i] = ranking[i].index;
			}
		}
		else{
			for (i = 0; i < topN; i++){
				printf("Score: %f\n", ranking[i].value);
				score[i] = ranking[i].index;
			}
		}

		printf("Done!\n\n");

		tGlob = clock() - tGlob;
		time_taken = ((double) tGlob) / CLOCKS_PER_SEC;
		printf("-- [C] Whole runtime: %f seconds --\n", time_taken);

		return score;
	}
""")

ffibuilder.cdef("""

	int compare_scores(const void *a, const void *b);

	int * scores(float Q[][200], float Docs[][200], int n, int Qn, int Dn, int score[], int topN);

	float euclid(float vec[200], int n);

	float dotprod(float vec1[200], float vec2[200], int n);

	float computeCosine(float query[200], float doc[200], int n, float normQuery, float normDoc);

	float desm(float Q[][200], float D[200], int n, int Qn, float normQuerys[], float normDoc);
""")

if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

