#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 17:15:03 2018

@author: wentingyang
"""
import pandas as pd
import numpy as np
df=pd.read_csv('5_Hotel_Unique.csv',sep=',')
df1.dtypes
df1=df.drop(['No.','Hotel_Unique','SentimentAnalysis_Label','Review','SentimentScore','duplicateuser(yes1/no0)','ContentSimilarity_Label','Hotel Name','Review Date','Headers','Username','Rating','Review_Answer','diff',], axis=1)
df1 = df1.reindex(['Num_reviews','Num_likes','countsverbs','countsnouns','duplicateusertimesaggregated','diff<=5','Overall_Label'], axis=1)
df1 = df1.rename(columns={'Num_reviews': 'Num_Reviews', 
                          'Num_likes':'Num_Likes',
                          'countsverbs':'Count_Verbs','countsnouns':'Count_Nouns',
                          'duplicateusertimesaggregated':'Num_Reviews_DuplicateUser',
                          'diff<=5':'Interval_Days5',
                          'Overall_Label':'Fake_Review'})
df2=df1(dict(yes=1,no=0))
class_mapping={label:idx for idx,label in enumerate(np.unique(df1['Interval_Days5']))}
df1['Interval_Days5']=df1['Interval_Days5'].map(class_mapping)
import seaborn as sns
sns.set(style='ticks')
colors = ["amber", "faded green"]
sns.pairplot(df1.dropna(),hue="Fake_Review", palette='deep')


sum(df1['Fake_Review'])-len(df1)


        
