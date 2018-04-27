from _cffi_desm import ffi, lib
import pickle
import numpy as np
import extract_word_embedds as ewe
##################################

m_path = "/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/data.txt"
outemb_path = '/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/out.txt'
inemb_path = '/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/in.txt'

'''
docs = ewe.get_doc_embedds(m_path, 5, outemb_path)

q = ewe.get_query_embedds("cambridge", inemb_path)[0]

#save embeddings for debugging purposes
with open('doc_embedds.obj', 'wb') as f:
	pickle.dump(docs, f)

with open('query_embedds.obj', 'wb') as f:
	pickle.dump(q, f)
'''

with open('doc_embedds.obj', 'rb') as f:
	docs = pickle.load(f)

with open('query_embedds.obj', 'rb') as f:
	q = pickle.load(f)

doc_title = ['Cambridge', 'Oxford', 'Giraffes', 'Giraffes_switched', 'Cambridge_switched', 'query']

#amount of Query-words (or queries?)
Qn = 1
#transform queries to lists
q = [q[0].tolist()]
#amount of word-vector-items
n = 200
#amount of Documents
Dn = len(docs)
ds = []
#transform documents to lists
for idx, d in enumerate(docs):
	ds.append(d.tolist())


scores = ffi.new("float["+str(Dn)+"]")

lib.scores(q, ds, n, Qn, Dn, scores)

for idx, score in enumerate(scores):
	print(doc_title[idx], str(score), '\n')

##################################
