#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 22:21:19 2018

@author: wentingyang
"""
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
import nltk
nltk.download('averaged_perceptron_tagger')
import pandas as pd
Dbase=pd.read_csv('5_Hotel_Unique.csv',sep=',')
Dbase=Dbase.loc[0:10,]
list_content=list(Dbase['Review'])




#count of verbs and nouns
def POS_Tagging(sentence):
    tagged_list = []
    tags = []
    count_verbs = 0
    count_nouns = 0
    text=nltk.word_tokenize(sentence)
    tagged_list = (nltk.pos_tag(text))
    
    tags = [x[1] for x in tagged_list]
    for each_item in tags:
        if each_item in ['VERB','VB','VBN','VBD','VBZ','VBG','VBP']:
            count_verbs+=1
        elif each_item in ['NOUN','NNP','NN','NUM','NNS','NP','NNPS']:
            count_nouns+=1
        else:
            continue
    return count_verbs,count_nouns

counts_vn=[]
for i in range(0,len(list_content)):
    counts_vn.append(POS_Tagging(list_content[i]))

counts=pd.DataFrame(counts_vn)

newdata=Dbase[['countsverbs','countsnouns','No.']]

Dbase['countsverbs']=counts[0]
Dbase['countsnouns']=counts[1]

newdata.to_csv('updatedcounts.csv',header=True)


