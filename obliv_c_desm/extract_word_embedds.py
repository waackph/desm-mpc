import numpy as np
import nltk
import pickle

#Tokenize Documents (documents are seperated by "\n\n" and terminated by "\n\n\n")
def tokenize_docs(path, amountDocs):
    #get documents (as a string) into a list
    f = open(path)
    docs = f.read().split('\n\n')[:amountDocs]
    f.close()
    #Tokenize documents
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    doc_list = []
    for idx, doc in enumerate(docs):
        doc = doc.lower()
        doc_list.append(tokenizer.tokenize(doc))
    #format numbers correctly for each document
    list_numb = []
    next_numb = False
    for doc in doc_list:
        numb = []
        for idx, word in enumerate(doc):
            if idx<len(doc)-1 and doc[idx].isdigit() and doc[idx+1].isdigit():
                numb.append(doc[idx] + '.' + doc[idx+1])
                next_numb = True
            elif next_numb:
                next_numb = False
                continue
            else:
                numb.append(word)
        list_numb.append(numb)
    return list_numb #doc_list


#build an offset index for each word in the embedding-file to later access the correct word-embedding using seek()
def build_embed_index(path):
    f = open(path)
    d = dict()
    offset = 0
    for idx, word in enumerate(f):
        if idx%1000000==0:
            print('Progress: Line ' + str(idx))
        d[word.split('\t')[0]] = offset
        offset += len(word)+1
    f.close()
    return d


#extract the word-vectors for each word in a document, yielding a list of word-vectors instead of the word itself per document
def extract_embed(file, dic, doc):
    fd = open(file)
    vecs = []
    for word in doc:
        if word not in dic.keys():
            continue
            #vecs.append(np.zeros(200))
        else:
            fd.seek(dic[word])
            w = fd.readline()
            vecs.append(np.array([float(i) for i in w.split('\t')[1:]]))
    fd.close()
    return vecs


#Compute Document-Centroid
#A function to compute the euclidean norm of a vector
def euclid_norm(v):
    norm = 0
    for i in v:
        norm += i**2
    return np.sqrt(norm)


#Compute the centroid of the word-vectors of a Document to get a Document-Vector
def compute_centroid(D):
    D_N = len(D)
    centroid = np.zeros(len(D[0]))
    for d in D:
        centroid += d / euclid_norm(d)
    return centroid/D_N


# Execution Function to get the document embeddings
def get_doc_embedds(path, amountDocs, model_dir, has_idx):
	outemb_path = model_dir + "out.txt"

	documents = tokenize_docs(path, amountDocs)

	if has_idx:
		idx_path = model_dir + "out_index.obj"
		with open(idx_path, 'rb') as f:
			out_dic = pickle.load(f)
	else:
		#Build index for out word-embeddings
		out_dic = build_embed_index(outemb_path)

	#Get word embeddings for each document, yielding the Data Structure: doc_embeds[doc][vec][item]
	doc_embeds = []
	for document in documents:
	    doc_embeds.append(extract_embed(outemb_path, out_dic, document))

	#Compute the document vectors by computing the centroid of the word-vectors of the document, yielding the data structure: doc_centroids[doc][entry]
	doc_centroids = []
	for embed in doc_embeds:
	    doc_centroids.append(compute_centroid(embed))
	
	return doc_centroids


# Execution Function to get the query-words embeddings
# Input: string as a query
def get_query_embedds(query, model_dir, has_idx):
	inemb_path = model_dir + "in.txt"

	#Get word embeddings for the query, resulting Data Structure: query_embeds[query][vec][item]
	tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
	q_tokens = tokenizer.tokenize(query)

	if has_idx:
		idx_path = model_dir + "in_index.obj"
		with open(idx_path, 'rb') as f:
			in_dic = pickle.load(f)
	else:
		#Build index for in word-embeddings
		in_dic = build_embed_index(inemb_path)


	query_embeds = []
	query_embeds.append(extract_embed(inemb_path, in_dic, q_tokens))

	return query_embeds


def get_embeddings(model_dir, inputs, has_idx, party, num_docs = 0):
	if party == 1:
		embeds = get_doc_embedds(inputs, num_docs, model_dir, has_idx)
	elif party == 2:
		embeds = get_query_embedds(inputs, model_dir, has_idx)
	return embeds


####Helper

def extract_vector_model_idx(filepath, target_path):
	idx_dic = build_embed_index(filepath)

	with open(target_path, 'wb') as f:
	    pickle.dump(idx_dic, f)
	
	print("Index extracted")


####Not used

#A function to compute the absolute/manhattan norm of a vector
def abs_norm(v):
    norm = 0
    for i in v:
        norm += abs(i)
    return norm


def desm(Q, D):
    #Denominator
    Q_N = len(Q)
    #Sum of cosine similarities between query term and document
    Q_cosine = 0
    for q in Q:
        qdot = q.dot(D)
        eucq = euclid_norm(q)
        eucD = euclid_norm(D)
        print(qdot, eucq, eucD)
        Q_cosine += qdot / eucq * eucD
    return Q_cosine/Q_N

