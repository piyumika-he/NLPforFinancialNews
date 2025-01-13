# -*- coding: utf-8 -*-

#Importing required libraries
import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd  
import re 



#function to scrape required variables, header, date, url and the full content of the article

def ob(webLink):
    i = 0

    #requesting the url from the relavant web server
    response_ob = requests.get(webLink)
    #getting the html code of requested website
    soup_ob = bs(response_ob.text)

    #getting the html codes of required news articles
    items = soup_ob.select('div.views-row')
    len(items)

    #creating the new list news
    news = []


    for item in items:
        #creating a new dictionary news_dict
        news_dict = {}
        
        #obtaining  the header of each of the required news article       
        try:
            news_dict['header'] = item.select('a')[1].text    
        
        except: 
            news_dict['header']  = item.select('a')[0].text   
        
        #obtaining the url for the web page where the full content of each article lays
        url = 'http://www.sundayobserver.lk'+item.select_one('a')['href']
        news_dict['url']=url
        
        #getting the html code of the webpage where full article is in
        response_url = requests.get(url)  
        soup_url = bs(response_url.text)
    
 
        #obtaining the date
        date = soup_url.findAll("span",{"class":["date-display-single"]})
        try:
            news_dict['date'] = date[5].text 
        
        except: 
            news_dict['date']  = 'None' 
        
        #obtaining the full content of the article
        x = soup_url.select('div.field-items')
        para = ' '.join([element.text for element in x])
        para_new = re.sub('[\n,\xa0,\t]', ' ',para )
    
        news_dict['body']=para_new
        i=i+1
      
        news.append(news_dict)
    return news



page_number=53
#creating a new variable
ob_news = []
#obtaining the news articles in the year 2018
for i in range(1,page_number):
    if(i<10):
        link = f'http://www.sundayobserver.lk/date/2018-W0{i}?field_section_tid=All'
    else:
        link = f'http://www.sundayobserver.lk/date/2018-W{i}?field_section_tid=All'
    print(link)
    news_items = ob(link)
    
    for j in news_items:
        ob_news.append(j)
        
#obtaining the news articles in the year 2019        
for i in range(1,page_number):
    if(i<10):
        link = f'http://www.sundayobserver.lk/date/2019-W0{i}?field_section_tid=All'
    else:
        link = f'http://www.sundayobserver.lk/date/2019-W{i}?field_section_tid=All'
    print(link)
    news_items = ob(link)
    
    for j in news_items:
        ob_news.append(j)
        

#obtaining the news articles in the year 2020        
for i in range(1,page_number):
    if(i<10):
        link = f'http://www.sundayobserver.lk/date/2020-W0{i}?field_section_tid=All'
    else:
        link = f'http://www.sundayobserver.lk/date/2020-W{i}?field_section_tid=All'
    print(link)
    news_items = ob(link)
    
    for j in news_items:
        ob_news.append(j)

#obtaining the news articles in the year 2021
#As there are only 7 weeks passed when this code implemented, page_number = 7 is used here   
#If you want to extract news articles in a specific month in 2021, observe the url of each web page you are required to scrape and
#change the variable page_number and the range of the for loop according to that.    
page_number =7        
for i in range(1,page_number):
    link = f'http://www.sundayobserver.lk/date/2021-W0{i}?field_section_tid=All'
    print(link)
    news_items = ob(link)
    
    for j in news_items:
        ob_news.append(j)
        
#creating a dataframe               
df = pd.DataFrame(ob_news) 

#appending the website name to the dataframe
df['website_name'] = 'Observer'

#saving the obtained dataframe 'df' in the 'News Index' folder as a csv file

df.to_csv(r'E:\\News Index\\Observer.csv') 
