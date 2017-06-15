# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:09:23 2017

@author: Junior
"""
import re
import os
import codecs
import pandas as pd
import jieba
import jieba.analyse


def main_func():
    filePaths = []
    contents = []
    sheep_articles = []
    sheep_paths = []
    tag1s = []
    tag2s = []
    tag3s = []
    
    for root , dirs, files in os.walk(r'..\data'):
        for name in files:
            filePath = os.path.join(root, name)
            f = codecs.open(filePath, 'r', 'utf-8')
            content = f.read().strip()
            f.close()
            # 匹配中文
            content1 = str()
            zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
            for item in zhPattern.findall(content):
                content1 += item
            # 确保能取到3个关键词 
            if len(content1) > 10:
                tags = jieba.analyse.extract_tags(content1, topK = 3)
                filePaths.append(filePath)
                contents.append(content1)
                tag1s.append(tags[0])
                tag2s.append(tags[1])
                tag3s.append(tags[2])
                
            # 找“羊毛”相关文章
            sheep = re.compile('羊')
            if sheep.search(content1):
                sheep_articles.append(content1)
                sheep_paths.append(filePath)
                
    tagDF = pd.DataFrame({
        'filePath': filePaths,
        'content': contents,
        'tag1': tag1s,
        'tag2': tag2s,
        'tag3': tag3s
    })
    
    tag_sheep = pd.DataFrame({
        'filePath': sheep_paths,
        'content': sheep_articles
    })
    tag_sheep.to_csv(r'..\output\tag_sheep.csv', index = False, header = False, encoding  = 'utf-8')


if __name__ == "__main__":
    main_func()
