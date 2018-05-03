import sys
import pickle
import numpy as np
from cffi import FFI
ffi = FFI()

##################################

party = int(sys.argv[1])
embedds_path = sys.argv[2]

with open(embedds_path, 'rb') as f:
	vecs = pickle.load(f)

#amount of word-vector-items
n = 200

if party == 1:
	#amount of Documents
	m = len(vecs)
	ds = []
	#transform documents to lists
	for idx, d in enumerate(vecs):
		ds.append(d.tolist())
	#print(ds[0])

if party == 2:
	#amount of Query-words (or queries?)
	m = 1
	#transform queries to lists
	ds = [vecs[0].tolist()]
	#Need to be known to keep scores alive after desm-Computation

Dn = 5


##########

ffi.cdef("""
	int * setup(int party, float vecs[][200], int amount, float scores[]);
""")

scores = ffi.new("float["+str(Dn)+"]")

desm = ffi.dlopen("/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/Umsetzung/desm-mpc/obliv_c_desm/old_v4/libdesm.so")

desm.setup(party, ds, m, scores)

##########

if party == 2:
	doc_title = ['Cambridge', 'Oxford', 'Giraffes', 'Giraffes_switched', 'Cambridge_switched', 'query']
	for idx, score in enumerate(scores):
		print(doc_title[idx], str(score), '\n')

##################################


