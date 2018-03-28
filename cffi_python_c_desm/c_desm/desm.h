#ifndef DESM_H_
#define DESM_H_

float euclid(float vec[3], int n);

float dotprod(float vec1[3], float vec2[3], int n);

float computeCosine(float query[3], float doc[3], int n);

float desm(float Q[][3], float D[3], int n, int Qn);

#endif // DESM_H_
