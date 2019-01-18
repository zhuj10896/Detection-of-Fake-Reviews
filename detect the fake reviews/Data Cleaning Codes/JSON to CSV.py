# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:36:09 2018

@author: Miguel
"""

import pandas as pd
import json

data = []
with open('Hyatt.json',encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('Lowes.json',encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))
        
with open('Mandarin_Oriental.json',encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('The_Ellis.json',encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))
        
with open('Whit.json',encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

master_data=pd.DataFrame.from_dict(data)
master_data.to_csv('Master_Data.csv')