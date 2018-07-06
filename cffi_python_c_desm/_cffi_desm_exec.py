from _cffi_desm import ffi, lib
import pickle
import numpy as np
import sys
import extract_word_embedds as extract
import time
##################################

# command: python3 _cffi_desm_exec.py ../../data/data.txt "cambridge"

# Measure runtime of processing steps
start_time = time.time()


########## Initilize global Variables

docs_path = sys.argv[1]
query_str = sys.argv[2]

#amount of top-ranked documents
top_n = 830

model_dir = "../../model/"
has_model_idx = True


########## Initilize Word-Vectors and compute Document-Centroids

print("Retrieve word-vectors and compute document vectors")

doc_vecs = extract.get_doc_embedds(docs_path, model_dir, has_model_idx)
ds = []
#transform documents to lists
for idx, d in enumerate(doc_vecs):
	ds.append(d.tolist())

query_vecs = extract.get_query_embedds(query_str, model_dir, has_model_idx)[0]
qs = []
#transform query-words to lists
for idx, q in enumerate(query_vecs):
	qs.append(q.tolist())

titles = extract.get_titles(docs_path)

Dm = len(ds)
Qm = len(qs)
n = len(ds[0])

print("-- [python] Whole Initilization for C-Program: %s seconds --" % (time.time() - start_time))


########## C Initilization and Execution

c_start_time = time.time()

print("Begin C-Score Computation")

scores = ffi.new("int[%d]" % top_n)

lib.scores(qs, ds, n, Qm, Dm, scores, top_n)

print("-- [python] C-Program runtime: %s seconds --" % (time.time() - c_start_time))

########## Output

print("Get position of relevant Documents in Ranking:")

relevant_idx = []
rel_amount = 10

rel_start = 350
for i in range(rel_start, rel_start + rel_amount): #range(top_n-1):
	relevant_idx.append(i)

rel_start = 610
for i in range(rel_start, rel_start + rel_amount):
	relevant_idx.append(i)

scores_py = ffi.unpack(scores, top_n)
score_pos = []
for idx in relevant_idx:
	print(str(idx), scores_py.index(idx))
	score_pos.append(scores_py.index(idx))

print("Median of Ranking-Result:", np.median(score_pos))

#for idx in scores:
#	print(str(idx), titles[idx])


print("-- [python] Whole runtime: %s seconds --" % (time.time() - start_time))

##################################
