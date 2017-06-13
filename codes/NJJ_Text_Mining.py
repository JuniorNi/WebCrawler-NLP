# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:17:00 2017

@author: Junior
"""
import re
import os
import os.path
import codecs
import jieba
import pandas as pd
import numpy as np
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
os.getcwd()

# 创建语料库
def make_corpos():
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
    corpos = pd.DataFrame({'filePath': filePaths, 'fileContent': fileContents})
    
    return corpos


def split_zh(corpos):
    # 匹配中文
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    # 分词
    segments = []
    filePaths = []
    for index, row in corpos.iterrows():
        filePath = row['filePath']
        fileContent = row['fileContent']
        segs = jieba.cut(fileContent)
        for seg in segs:
            if zhPattern.search(seg):
                segments.append(seg)
                filePaths.append(filePath)
    segmentDataFrame = pd.DataFrame({'segment': segments, 'filePath': filePaths})  
    
    return segmentDataFrame


def freq_cnt(segmentDataFrame):
    #进行词频统计        
    segStat = segmentDataFrame["segment"].groupby(
                segmentDataFrame["segment"]
            ).agg({
                "计数":np.size
            }).reset_index().sort(
                columns=["计数"], ascending=False
            )
    # 移除停用词
    stopwords = pd.read_csv( r'.\data\StopwordsCN.txt', encoding='utf8',index_col=False)
    fSegStat = segStat[~segStat.segment.isin(stopwords.stopword)]
    
    return fSegStat

# 词云
def wordcloud(fSegStat):
    wordcloud = WordCloud(font_path = 'simhei.ttf', background_color = 'black')
    wordcloud = wordcloud.fit_words(fSegStat.itertuples(index = False))
    plt.imshow(wordcloud)
    
    # from scipy.misc import imread
    # import matplotlib.pyplot as plt
    # from wordcloud import WordCloud,ImageColorGenerator
    # bimg=imread(r'.\img\bt.png')
    # wordcloud=WordCloud(background_color="white",mask=bimg,font_path='simhei.ttf')
    # wordcloud=wordcloud.fit_words(fSegStat.itertuples(index=False))
    # bimgColors=ImageColorGenerator(bimg)
    # plt.axis("off")
    # plt.imshow(wordcloud.recolor(color_func=bimgColors))
    # plt.show()
    

def main():
    corpos = make_corpos()
    segmentDataFrame = split_zh(corpos)
    fSegStat = freq_cnt(segmentDataFrame)
    wordcloud(fSegStat)

# 当被import作为模块调用的时候，if以下的代码就不会被执行，也就是说main()函数不会被执行。
if __name__ == "__main__":
    main()
