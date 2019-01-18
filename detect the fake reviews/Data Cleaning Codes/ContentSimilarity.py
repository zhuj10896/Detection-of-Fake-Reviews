#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 14:24:04 2018
content similarity
@author: wentingyang
"""

import pandas as pd
import numpy as np

Dbase=pd.read_csv('Master_Data.csv',sep=',')


list_content=list(Dbase['Review'])


import gensim
print(dir(gensim))
raw_documents = list_content
print("Number of documents:",len(raw_documents))

#import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
gen_docs = [[w.lower() for w in word_tokenize(text)] 
            for text in raw_documents]
print(gen_docs)


dictionary = gensim.corpora.Dictionary(gen_docs)

print("Number of words in dictionary:",len(dictionary))
for i in range(len(dictionary)):
    print(i, dictionary[i])
    

corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
print(corpus)


tf_idf = gensim.models.TfidfModel(corpus)
print(tf_idf)
s = 0
for i in corpus:
    s += len(i)
print(s)


sims = gensim.similarities.Similarity('/Users/wentingyang/Downloads',tf_idf[corpus],
                                      num_features=len(dictionary))
print(sims)
print(type(sims))

    
label=[]
for text_content in list_content: 
    query_doc = [w.lower() for w in word_tokenize(text_content)]
    #print(query_doc)
    query_doc_bow = dictionary.doc2bow(query_doc)
    #print(query_doc_bow)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    #print(query_doc_tf_idf)
    
    sims[query_doc_tf_idf]
    #max(sims[query_doc_tf_idf])
    test=list(enumerate(sims[query_doc_tf_idf]))
    max_test=sorted(test,key=lambda tup:tup[1],reverse=True)[1][1]
    #max_test=max_test[1]
    if max_test<.5:
        Label_score=True
    else:
        Label_score=False
    label.append(Label_score)


sentiment=pd.read_csv("results_joined_sentiment.csv")
sentiment['SIM_label']=label

sentiment['Overall_label']=True

for i in range(sentiment.shape[0]):
    sentiment.iat[i,-1]=sentiment.iat[i,-2] and sentiment.iat[i,-3]
    
from datetime import datetime

def try_parsing_date(text):
    for fmt in ('%d-%b-%y','%B %d, %Y'):
        try: 
            return datetime.strptime(text.strip(),fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

sentiment.iat[1021,2]='October 28, 2018'
sentiment['Review Date']=sentiment['Review Date'].apply(lambda x:try_parsing_date(x))

#sentiment.drop(['Review Date_corrected'],axis=1)


sentiment.to_csv('FinalData.csv',header=True)

























