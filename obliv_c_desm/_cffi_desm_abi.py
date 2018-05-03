import sys
import pickle
import numpy as np
import extract_word_embedds as extract
from cffi import FFI
ffi = FFI()

########## Initilize global Variables

party = int(sys.argv[1])
# Local: ../../model/
model_dir = sys.argv[2]
# True
has_model_idx = bool(sys.argv[3])

########## Initilize Word-Vectors and compute Document-Centroids

if party == 1:
	# Local: ../../data/data.txt
	docs_path = sys.argv[4]
	vecs = extract.get_embeddings(model_dir, docs_path, has_model_idx, party, 5)
elif party == 2:
	# cambridge
	query_str = sys.argv[4]
	vecs = extract.get_embeddings(model_dir, query_str, has_model_idx, party)
else:
	print("Party not defined or wrong number (only 1 or 2 possible)")


#amount of word-vector-items
Dn = 5

if party == 1:
	#amount of Documents
	ds = []
	#transform documents to lists
	for idx, d in enumerate(vecs):
		ds.append(d.tolist())
if party == 2:
	#transform queries to lists
	ds = []
	for idx, d in enumerate(vecs[0]):
		ds.append(d.tolist())
	#amount of Query-words (or queries?)

m = len(ds)
n = len(ds[0])

print(m, n)



########## oblivc Initilization and Execution

ffi.cdef("""
	int * setup(int party, float vecs[][200], int amount, int n, float scores[]);
""")

scores = ffi.new("float["+str(Dn)+"]")

desm = ffi.dlopen("/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/Umsetzung/desm-mpc/obliv_c_desm/libdesm.so")

desm.setup(party, ds, m, n, scores)

########## Output

if party == 2:
	doc_title = ['Cambridge', 'Oxford', 'Giraffes', 'Giraffes_switched', 'Cambridge_switched']
	for idx, score in enumerate(scores):
		print(doc_title[idx], str(score), '\n')

##########
