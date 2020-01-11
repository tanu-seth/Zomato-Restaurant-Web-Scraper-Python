# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 00:15:48 2020

@author: tanus
"""

import requests
from bs4 import BeautifulSoup
import pandas
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# set the iterator pagenumber to automate crawling over given number of pages
pagenum = 1
rest_list =[]

for page in range(1,191):
    
    # set the url for zomato cincinnati restaurants as requests.get parameter 
    response = requests.get("https://www.zomato.com/cincinnati/restaurants?page={0}".format(pagenum), headers=headers)
    content = response.content
    
    # use BeautifulSoup for pulling data out of html files
    soup = BeautifulSoup(content, "html.parser")
    
    search_list = soup.find_all("div", {'id': 'orig-search-list'})
    
    # filtering all the div that has restaurant data stored
    list_content = search_list[0].find_all("div", {'class': 'content'})
    
    # iterating 15 times as there are 15 restaurants listed on each page
    for i in range(0,15):
        
        data={} 
        
        data['rest_name'] = list_content[i].find("a", {'data-result-type': 'ResCard_Name'}).text.replace('\n', ' ').strip()
        
        data['locality'] = list_content[i].find("b").text.replace('\n',' ').strip()
        
        
        ratings = list_content[i].find("div", {'data-variation': 'mini inverted'})
        # ignoring the restaurant where we dont have any rating available
        if ratings is None:
            continue
        data['ratings']=ratings.text.replace('\n',' ').strip()
        
        data['rest_id']= ratings['data-res-id']
        
        rest6 = list_content[i].find_all("div", {'class': 'search-page-text clearfix row'})
        rest7 = rest6[0].find_all("span", {'class': 'col-s-11 col-m-12 nowrap pl0'})
        rest8 = rest7[0].find_all("a")
        data['cuisines'] = [e.string for e in rest8]
        
        rest9 = rest6[0].find("span", {'class': 'col-s-11 col-m-12 pl0'})
        # ignoring the restaurant where we dont have cost_for_two available
        if rest9 is None:
            continue
        l=rest9.find_all('span',{'class':'cft_bold'})
        data['cost_for_two']=''.join(i.text for i in l)
        
        # ignoring the restaurant where we dont have votes available
        votes = list_content[i].find("span", {'class': re.compile(r'rating-votes-div*')})
        if votes is None:
            continue
        data['votes']=votes.text.split()[0].strip()
        
        #appending the data scraped for a restaurant to rest_list
        rest_list.append(data)
        
    print('scraped page {0}'.format(pagenum))
    pagenum+=1


# saving results to a dataframe
    
df = pandas.DataFrame(rest_list)
df = df[['rest_id','rest_name','locality','cuisines','cost_for_two','ratings','votes']]

# saving as csv

df.to_csv("zomato_restaurants_Cincinnati.csv")
