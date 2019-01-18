# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:18:20 2018

@author: Miguel
"""

import pandas as pd

import numpy as np

def prepare_text_for_lda(text):
    tokens = tokenizer.tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if not token.isnumeric()]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [token for token in tokens if token not in custom_stop_list]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

DataTotal=pd.read_csv("Hotel_Unique.csv")

DataB=DataTotal[DataTotal['Overall_Label']==False]

dict_w={}
for text in DataB['Review']:
    for word in prepare_text_for_lda(text):
        if word in dict_w:
            dict_w[word]=dict_w[word]+1
        else:
            dict_w[word]=1

counter_pandas=pd.DataFrame.from_dict(dict_w,orient='index',columns=['frequency'])
counter_pandas=counter_pandas.sort_values(by='frequency',ascending=False)
counter_pandas['word']=counter_pandas.index
Suspc_words=list(counter_pandas[:150]['word'])

DataTotal['Count_Susp_words']=0
for i in range(DataTotal.shape[0]):
    count_w=0
    for word in prepare_text_for_lda(DataTotal.iat[i,7]):
        if word in Suspc_words:
            count_w=count_w+1
    DataTotal.iat[i,-1]=count_w

for j in Suspc_words:
    DataTotal[j]=0
    for i in range(DataTotal.shape[0]):
        count_w=0
        for word in prepare_text_for_lda(DataTotal.iat[i,7]):
            if word==j:
                count_w=count_w+1
        DataTotal.iat[i,-1]=count_w
        
DataTotal.to_csv("Hotel_Unique_Complete.txt",sep=',')

DataTotal.drop(['Hotel Name','Review Date','Username','Headers','Rating','Review','Review_Answer','SentimentScore','SentimentAnalysis_Label','ContentSimilarity_Label','duplicateuser(yes1/no0)','diff'],axis=1,inplace=True)

class_mapping={label:idx for idx,label in enumerate(np.unique(DataTotal['diff<=5']))}
DataTotal['diff<=5']=DataTotal['diff<=5'].map(class_mapping)

DataTotalNormalized=DataTotal.apply(lambda x: (x-min(x))/(max(x)-min(x)),axis=0)


X=DataTotal.drop(['Overall_Label'],axis=1)
X=X.apply(lambda x: (x-min(x))/(max(x)-min(x)),axis=0)

from sklearn.model_selection import train_test_split
y=DataTotal['Overall_Label']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33,random_state=0)

X_test.to_csv("X_test_complete.csv",index=False)
X_train.to_csv("X_train_complete.csv",index=False)
y_test.to_csv("y_test_complete.csv",index=False)
y_train.to_csv("y_train_complete.csv",index=False)
y_train.shape

X_train.index[np.isnan(X_train).any(1)]
X_train.columns.to_series()[np.isnan(X_train).any()]

X_test.fillna(0,inplace=True)

