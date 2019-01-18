# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 22:42:02 2018

@author: Miguel
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

#import data
DBase=pd.read_csv("Master_Data.csv")

#sentiment score
DBase['SentimentScore']=DBase['Review'].apply(lambda x:analyser.polarity_scores(x)['compound'])
DBase['Label_Sentiment']=False

#Sentiment Label
def sentiment_label_if(score_x,rating_x):
    if((rating_x>=4 and score_x<0) or (rating_x<=2 and score_x>0)):
        return False
    else:
        return True

for i in range(DBase.shape[0]):
    DBase.iat[i,-1]=sentiment_label_if(DBase.iat[i,-2],DBase.iat[i,5])

DBase.to_csv("results_joined_sentiment.csv",index=False)


