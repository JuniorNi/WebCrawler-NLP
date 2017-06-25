# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 22:03:51 2017
@author: Junior
我爱卡神：http://bbs.creditcard.com.cn/forum-170-1.html
"""

from bs4 import BeautifulSoup
import requests
import random
# import pandas as pd
from time import sleep
from pandas import Series, DataFrame
import pandas as pd

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Referer': 'http://www.kashen8.com/core/bankcomm/'}
    

def get_websites(page_start,page_end):
    data = []
    for i in range(page_start,page_end):
        url       = 'http://bbs.creditcard.com.cn/forum-170-{}.html'.format(str(i))
        # print('正在读取第{}页'.format(str(i)))
        # print(url)
        sleep(1*random.uniform(1,3))   
        
        wb_data   = session.get(url, headers=headers)
        soup      = BeautifulSoup(wb_data.text,'lxml')
        websites  = soup.select(" tr > th > a.s.xst")        # 网址与标题
        titles    = soup.select(" tr > th > a.s.xst")         
        req_times = soup.select("tr > td > em > span")       # 发帖与最后回复时间
        res_times = soup.select("tr > td > em > a")
        res_cnts  = soup.select("tr > td.num > a")           # 回复数与查看数
        look_cnts = soup.select("tr > td.num > em")
        
        for website,title,req_time,res_time,res_cnt,look_cnt in zip(websites,titles,req_times,res_times,res_cnts,look_cnts) :
            info = {
                "website" :  website.get("href"),
                "title"   :  title.get_text(),
                "req_time":  req_time.get_text(),
                "res_time":  res_time.get_text(),
                "res_cnt" :  res_cnt.get_text(),
                "look_cnt":  look_cnt.get_text()      
            }
            data.append(info)
        print('已完成第{}页'.format(str(i))) 
    
    df = DataFrame(data,columns = ['website','title','req_time','res_time','res_cnt','look_cnt'])
    # df.index.name = 'index'
    df.to_csv(r'.\output\test3\get_websites.txt', encoding = 'utf-8', index = False)
    return df


#############################################################################
'''
data2 - [0:1000]
data3 - [1000:1080]
data1 - [1080:2405]
'''
data2 = []
data3 = []
def get_content(df1):
    df1 = df1[1000:1080]
    for index, row in df1.iterrows():
        url      = row['website']
        title    = row['title']
        sleep( 1 * random.uniform(1,3) )       
        wb_data  = session.get(url, headers=headers)
        soup     = BeautifulSoup(wb_data.text,'lxml')
        contents = soup.findAll('td', {'class': 't_f'}) 
        
        if len(contents) > 0:
            info = {
                'website': url, 
                'title'  : title, 
                'content': contents[0].get_text()
            }
        else:
            info = {
                'website': url, 
                'title'  : title, 
                'content': '无'
            }
            
        # info_series = Series(info, index = ['website','title','content'])
        # 每个帖子一个txt文件
        # info_series.to_csv(r'.\output\test3\content\text{}.txt'.format(str(index)), encoding = 'utf8')
        
        data3.append(info)
        print('已完成第{}个'.format(str(index))) 
              
    df2 = DataFrame(data2, columns = ['website','title','content'])
    df2.to_csv(r'.\output\test3\websites_content.txt', encoding = 'utf-8', index = False)
    return df2    



if __name__ == '__main__':   
    df1 = get_websites(1,101)
    # df1 = pd.read_csv(r'.\output\test3\get_websites.txt', encoding = 'utf8',index_col  =False)
    df2 = get_content(df1[0:1080])
    df3 = get_content(df1[1080:])


