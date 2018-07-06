import sys
import time
import pickle
import numpy as np
import extract_word_embedds as extract
from cffi import FFI
ffi = FFI()

# command party 1: python3 _cffi_desm_abi.py 1 ../../model/ True ../../data/data.txt
# command party 2: python3 _cffi_desm_abi.py 2 ../../model/ True "cambridge" ../../data/data.txt

# Measure runtime of processing steps
start_time = time.time()

########## Initilize global Variables

party = int(sys.argv[1])
# Local: ../../model/
model_dir = sys.argv[2]
# True
has_model_idx = bool(sys.argv[3])

########## Initilize Word-Vectors and compute Document-Centroids

print("Retrieve word-vectors and compute document vectors")

#amount of top-ranked documents
top_n = 0

if party == 1:
	# Local: ../../data/data.txt
	docs_path = sys.argv[4]
	vecs = extract.get_embeddings(model_dir, docs_path, has_model_idx, party)
elif party == 2:
	# cambridge
	query_str = sys.argv[4]
	top_n = 2 #sys.argv[5]
	vecs = extract.get_embeddings(model_dir, query_str, has_model_idx, party)[0]
	titles = extract.get_titles(sys.argv[5])
else:
	print("Party not defined or wrong number (only 1 or 2 possible)")

if party == 1:
	#amount of Documents
	ds = []
	#transform documents to lists
	for idx, d in enumerate(vecs):
		ds.append(d.tolist())
if party == 2:
	#transform queries to lists
	ds = []
	for idx, d in enumerate(vecs):
		ds.append(d.tolist())
	#amount of Query-words (or queries?)

m = len(ds)
n = len(ds[0])

print("Dimensions:", m, n)

print("-- [python] Whole Initilization for C-Program: %s seconds --" % (time.time() - start_time))

########## oblivc Initilization and Execution

c_start_time = time.time()

ffi.cdef("""
	int * setup(int party, float vecs[][200], int amount, int n, int *scores, int topN);
""")

scores = ffi.new("int[%d]" % top_n)

#Dynamically allocating 2-dim Array (does not work yet..)
#vectors = ffi.new("float* [%d]" % m)
#for i in range(m):
#	vectors[i] = ffi.new("float[%d]" % n)

#for i in range(m):
#	for j in range(n):
#		vectors[i][j] = ds[i][j]

desm = ffi.dlopen("/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/Umsetzung/desm-mpc/obliv_c_desm/libdesm.so")

desm.setup(party, ds, m, n, scores, top_n)

print("-- [python] C-Program runtime: %s seconds --" % (time.time() - c_start_time))

########## Output

if party == 2:
	for idx in scores:
		print(str(idx), titles[idx])
		#print(doc_title[idx], str(score), '\n')

print("-- [python] Whole runtime: %s seconds --" % (time.time() - start_time))

##########
