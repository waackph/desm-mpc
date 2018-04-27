from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_cffi_desm",
r""" 
	#include <stdio.h>
	#include <math.h>

	float euclid(float vec[200], int n){
		float norm = 0;
		int i = 0;
		//int n = sizeof(vec)/sizeof(float);
		for(i = 0; i < n; i = i+1){
			norm = norm + vec[i]*vec[i];
		}
		//return sqrt(norm);
		return norm;
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

	float computeCosine(float query[200], float doc[200], int n){
		float dotDoc = dotprod(query, doc, n);
		float normDoc = euclid(doc, n);
		float normQuery = euclid(query, n);
		//printf("%f\n%f\n%f\n", dotDoc, normDoc, normQuery);
		return dotDoc / normQuery * normDoc;
	}

	float desm(float Q[][200], float D[200], int n, int Qn){
		//int Qn = sizeof(Q)/sizeof(float);
		int i;
		float newCosine;
		float cosine = 0.0;
		//printf("%d\n", n);
		//printf("%d\n", Qn);
		for(i = 0; i < Qn; i = i+1){
			newCosine = computeCosine(Q[i], D, n);
			cosine = cosine + newCosine;
		}
		return cosine/Qn;
	}
	
	//args: queries as word-vectors, documents as word-vectors, len(word-vec), amount queries, amount Docs
	float * scores(float Q[][200], float Docs[][200], int n, int Qn, int Dn, float score[]){
		int i;
		for(i=0; i<Dn; i = i+1){
			score[i] = desm(Q, Docs[i], n, Qn);
		}
		return score;
	}
""")

ffibuilder.cdef("""

	float * scores(float Q[][200], float Docs[][200], int n, int Qn, int Dn, float score[]);

	float euclid(float vec[200], int n);

	float dotprod(float vec1[200], float vec2[200], int n);

	float computeCosine(float query[200], float doc[200], int n);

	float desm(float Q[][200], float D[200], int n, int Qn);
""")

if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

