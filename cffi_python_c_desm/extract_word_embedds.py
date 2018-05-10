import numpy as np
import nltk
import pickle
import re

import time

#nltk.download("stopwords")

#from nltk.corpus import stopwords

# Globally define symbols that should be removed or replaced
# define punctuation
punct = './;:()&+?!,'
punct_tok = ['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']',
                      '{', '}', '-', '–', '+', '*', '--', '\'\'', '``', '|', '%', '!', '?']

punct_sent_remove = '\''
punct_sent_space = '_/'

url_token = "http\S+"

encoding_errors = {"&amp;":'&', "&#39":'\''}

# A big stopword list would reduce processing time (less word-vectors) but maybe remove semantic information
#stop_words = set(stopwords.words('english'))
stop_words = ["the", "a"]


def get_documents(path, data_format):
    if data_format is "custom":
        with open(path) as f:
            docs = f.read().split("#!newDoc!#")
        return docs        
    if data_format is "csv":
        pass
    if data_format is "files":
        pass
    if data_format is "list":
        return path


def preprocess_tokens(tokens):
    # Preprocess on token level
    tokens = [tok for tok in tokens if tok not in punct_tok]
    tokens = [re.sub('[{}]'.format(punct), '', tok) for tok in tokens]
    tokens = [tok for tok in tokens if len(tok) > 1 or tok is "i"] #or tok.isdigit()]
    tokens = [tok for tok in tokens if tok not in stop_words]
    # Should digits be removed?
    tokens = [tok for tok in tokens if not tok.isdigit()]

    return tokens


def preprocess_sentence(sentence):
    # Preprocess on sentence level
    for encoding in list(encoding_errors.keys()):
        sentence = sentence.replace(encoding, encoding_errors[encoding])
    sentence = re.sub('{}'.format(url_token), ' ', sentence)
    sentence = re.sub('[{}]'.format(punct_sent_remove), '', sentence)
    sentence = re.sub('[{}]'.format(punct_sent_space), ' ', sentence)

    tokens = preprocess_tokens(nltk.tokenize.word_tokenize(sentence))
    
    return tokens


#Tokenize Documents (documents are per default seperated by "#!newDoc!#" and terminated by "\n\n\n")
def preprocess_docs(path, data_format="custom"):
    
    # extract documents from file(s)
    docs = get_documents(path, data_format)

    #Tokenize documents into sentences
    preprocessed_docs = []
    for idx, doc in enumerate(docs):
        # Preprocessing on document level
        doc = doc.lower()
        
        # Preprocessing on sentence level
        sentences = nltk.tokenize.sent_tokenize(doc)
        
        preprocessed_sentence = []
        for sent_idx, sent in enumerate(sentences):
            preprocessed_sentence += preprocess_sentence(sent)
        
        # Append preprocessed sentences to new list
        preprocessed_docs.append(preprocessed_sentence)

    return preprocessed_docs


# build an offset index for each word in the embedding-file to later access the correct word-embedding using seek()
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


# extract the word-vectors for each word in a document, yielding a list of word-vectors instead of the word itself per document
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


# Compute Document-Centroid
# A function to compute the euclidean norm of a vector
def euclid_norm(v):
    norm = 0
    for i in v:
        norm += i**2
    return np.sqrt(norm)


# Compute the centroid of the word-vectors of a Document to get a Document-Vector
def compute_centroid(D):
    D_N = len(D)
    centroid = np.zeros(len(D[0]))
    for d in D:
        centroid += d / euclid_norm(d)
    return centroid/D_N


# Get the document titles and their associated indices
def get_titles(path, data_format="custom"):

    start_time = time.time()

    titles = {}
    
    # extract documents from file(s)
    docs = get_documents(path, data_format)

    # Tokenize Document to get title
    for idx, doc in enumerate(docs):

        # Preprocessing on sentence level
        sentences = nltk.tokenize.sent_tokenize(doc)
        
        # Get title of document
        title = sentences[0].splitlines()
        title = [tok for tok in title if tok is not ""]
        titles[idx] = title[0]

    print("-- [query] Extract doc. titles: %s seconds --" % (time.time() - start_time))

    return titles


# Execution Function to get the document embeddings
def get_doc_embedds(path, model_dir, has_idx):

	# Measure runtime of processing steps
	start_time = time.time()

	outemb_path = model_dir + "out.txt"

	documents = preprocess_docs(path)

	print("-- [docs] Preprocessing: %s seconds --" % (time.time() - start_time))

	start_time = time.time()

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

	print("-- [docs] Retrieve word-vectors: %s seconds --" % (time.time() - start_time))

	start_time = time.time()

	#Compute the document vectors by computing the centroid of the word-vectors of the document, yielding the data structure: doc_centroids[doc][entry]
	doc_centroids = []
	for embed in doc_embeds:
	    doc_centroids.append(compute_centroid(embed))
	
	print("-- [docs] Compute Centroids: %s seconds --" % (time.time() - start_time))

	return doc_centroids


# Execution Function to get the query-words embeddings
# Input: string as a query
def get_query_embedds(query, model_dir, has_idx):

	# Measure runtime of processing steps
	start_time = time.time()

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

	print("-- [query] Preprocess & Retrieve word-vectors: %s seconds --" % (time.time() - start_time))

	return query_embeds


def get_embeddings(model_dir, inputs, has_idx, party):
	if party == 1:
		embeds = get_doc_embedds(inputs, model_dir, has_idx)
		return embeds
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

# A function to compute the absolute/manhattan norm of a vector
def abs_norm(v):
    norm = 0
    for i in v:
        norm += abs(i)
    return norm


def desm(Q, D):
    # Denominator
    Q_N = len(Q)
    # Sum of cosine similarities between query term and document
    Q_cosine = 0
    for q in Q:
        qdot = q.dot(D)
        eucq = euclid_norm(q)
        eucD = euclid_norm(D)
        print(qdot, eucq, eucD)
        Q_cosine += qdot / eucq * eucD
    return Q_cosine/Q_N

