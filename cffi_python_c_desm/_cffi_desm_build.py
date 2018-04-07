from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_cffi_desm",
r""" 
	#include <stdio.h>
	#include <math.h>

	double euclid(double vec[200], int n){
		double norm = 0;
		int i = 0;
		//int n = sizeof(vec)/sizeof(double);
		for(i = 0; i < n; i = i+1){
			norm = norm + vec[i]*vec[i];
		}
		return sqrt(norm);
	}

	double dotprod(double vec1[200], double vec2[200], int n){
		double sum = 0;
		int i = 0;
		//int n = sizeof(vec1)/sizeof(double);
		for(i = 0; i < n; i = i+1){
			//printf("%d\n%f\n%f\n\n", i, vec1[i], vec2[i]);
			sum = sum + vec1[i]*vec2[i];
		}
		return sum;
	}

	double computeCosine(double query[200], double doc[200], int n){
		double dotDoc = dotprod(query, doc, n);
		double normDoc = euclid(doc, n);
		double normQuery = euclid(query, n);
		//printf("%f\n%f\n%f\n", dotDoc, normDoc, normQuery);
		return dotDoc / normQuery * normDoc;
	}

	double desm(double Q[][200], double D[200], int n, int Qn){
		//int Qn = sizeof(Q)/sizeof(double);
		int i;
		double newCosine;
		double cosine = 0.0;
		//printf("%d\n", n);
		//printf("%d\n", Qn);
		for(i = 0; i < Qn; i = i+1){
			newCosine = computeCosine(Q[i], D, n);
			cosine = cosine + newCosine;
		}
		return cosine/Qn;
	}
	
	//args: queries as word-vectors, documents as word-vectors, len(word-vec), amount queries, amount Docs
	double * scores(double Q[][200], double Docs[][200], int n, int Qn, int Dn, double score[]){
		int i;
		for(i=0; i<Dn; i = i+1){
			score[i] = desm(Q, Docs[i], n, Qn);
		}
		return score;
	}
""")

ffibuilder.cdef("""

	double * scores(double Q[][200], double Docs[][200], int n, int Qn, int Dn, double score[]);

	double euclid(double vec[200], int n);

	double dotprod(double vec1[200], double vec2[200], int n);

	double computeCosine(double query[200], double doc[200], int n);

	double desm(double Q[][200], double D[200], int n, int Qn);
""")

if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

