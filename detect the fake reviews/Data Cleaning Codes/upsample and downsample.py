#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 19:33:28 2018
upsampling and downsampling
@author: wentingyang
"""
import numpy as np
df=pd.read_csv("Hotel_Unique_Complete.txt",sep=',')

X = df.drop(['Overall_Label'],axis=1)

# Create target vector
y = df['Overall_Label']
y = np.where((y == 0), 0, 1)

df_majority = df[y==1]
df_minority = df[y==0]
 
from sklearn.utils import resample
# Downsample majority class
df_majority_downsampled = resample(df_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=len(df_minority),     # to match minority class
                                 random_state=123) # reproducible results
df_downsampled = pd.concat([df_majority_downsampled, df_minority])
df_downsampled.to_csv('downsample.csv',header=True)
# Combine minority class with downsampled majority class
df_downsampled = pd.concat([df_majority_downsampled, df_minority])
sum(df_downsampled['Overall_Label'])

#upsample
df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority),    # to match majority class
                                 random_state=2000) # reproducible results
 
# Combine majority class with upsampled minority class
df_upsampled = pd.concat([df_majority, df_minority_upsampled])

 
df_upsampled.to_csv('upsample.csv',header=True)
