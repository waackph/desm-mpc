//Input: 2-Dim. Array[query][wordvec-item] Q
//Input: 1-Dim. Array[docvec-item] D
//Output: Float score

#include <stdio.h>
#include "desm.h"

float euclid(float vec[3], int n){
	int norm = 0;
	int i = 0;
	//int n = sizeof(vec)/sizeof(float);
	for(i = 0; i < n; i = i+1){
		norm = norm + vec[i]*vec[i];
	}
	return norm;
}

float dotprod(float vec1[3], float vec2[3], int n){
	int sum = 0;
	int i = 0;
	//int n = sizeof(vec1)/sizeof(float);
	printf("%d\n", n);
	for(i = 0; i < n; i = i+1){
		sum = sum + vec1[i]*vec2[i];
	}
	return sum;
}

float computeCosine(float query[3], float doc[3], int n){
	float dotDoc = dotprod(query, doc, n);
	float normDoc = euclid(doc, n);
	float normQuery = euclid(query, n);
	printf("%f\n%f\n%f\n", dotDoc, normDoc, normQuery);
	return dotDoc / normQuery * normDoc;
}

float desm(float Q[][3], float D[3], int n, int Qn){
	//int Qn = sizeof(Q)/sizeof(float);
	int i;
	float newCosine;
	float cosine = 0.0;
	float normDocs[3];
	float normQueries[3];
	for(..){
		normDocs[i] = euclid(doc, n);
		normQuerys[i] = euclid(query, n);
	}
	for(i = 0; i < Qn; i = i+1){
		newCosine = computeCosine(Q[i], D, n, normDocs, normQuerys);
		cosine = cosine + newCosine;
	}
	return cosine;
}


