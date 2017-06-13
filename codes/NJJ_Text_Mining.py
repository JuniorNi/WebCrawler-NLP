# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:17:00 2017

@author: Junior
"""

import os
import os.path
import codecs
import pandas as pd
os.getcwd()

path = r'E:\blog_知识储备\jieba分词\WebCrawler-NLP\data'
filePaths = []
fileContents = []
for root, dirs, files in os.walk(path):
    for name in files:
        filePath = os.path.join(root, name)
        filePaths.append(filePath)
        f = codecs.open(filePath, 'r', 'utf-8')
        fileContent = f.read()
        f.close()
        fileContents.append(fileContent)
        
corpos = pd.DataFrame({
    'filePath': filePaths,
    'fileContent': fileContents
})


   
import jieba

segments = []
filePaths = []
for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)
    for seg in segs:
        segments.append(seg)
        filePaths.append(filePath)

segmentDataFrame = pd.DataFrame({
    'segment': segments, 
    'filePath': filePaths
})


import numpy as np
#进行词频统计        
segStat = segmentDataFrame.groupby(
            by="segment"
        )["segment"].agg({
            "计数":numpy.size
        }).reset_index().sort(
            columns=["计数"],
            ascending=False
        );


