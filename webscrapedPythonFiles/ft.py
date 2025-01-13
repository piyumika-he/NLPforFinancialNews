# -*- coding: utf-8 -*-


#importing libraries
import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

#function to scrape required variables, header, date, url and the full content of the article
def ft(webLink):

    #getting the html code of required webpage
    response_ft = requests.get(webLink)
    soup_ft = bs(response_ft.text)

    #getting the html codes of required news articles
    items = soup_ft.select('div.col-md-6')
    len(items)

    #creating a new variable news
    news = []


    for item in items:
        #creating a new dictionary news_dict
        news_dict = {}
        
        #obtaining the header
        news_dict['header'] = item.select_one('h3').text
        
        #obtaining the url
        url = item.select_one('a')['href']
        news_dict['url']=url
        
        #getting the html code of the webpage where full article is in
        response_url = requests.get(url)  
        soup_url = bs(response_url.text)
    
 
        #obtaiining the date
        date = soup_url.find("span",{"class":["gtime"]}).text
        news_dict['date']=date
        
        #obtaining the full content of the article
        x = soup_url.select('header.inner-content')
        para = ''.join([element.text for element in x])
        para_new = re.sub('[\n,\xa0,\t]', ' ',para )
    
        news_dict['body']=para_new
      
        #appending extracted records to the news variable
        news.append(news_dict)
    return news

#the value assigns to 'page_number' variable should be changed accordingly. The number of pages where the required articles are in, have to be assigned to the variable
page_number=13

#creating a new variable to store scraped data.
ft_news = []
for i in range(0,page_number):
    number = i*30
    #obtaining business news articles of the daily FT news paper
    link = f'http://www.ft.lk/business/34/{number}'
    #obtaining entrepreneurship news articles of the daily FT news paper
    # link = f'http://www.ft.lk/entrepreneurship/41/{number}'
    #obtaining financial news articles of the daily FT news paper
    # link = f'http://www.ft.lk/financial-services/42/{number}'
    news_items = ft(link)
    
    for j in news_items:
        ft_news.append(j)
        

#In order to obtain the entrepreneurship news articles of daily FT News paper, make the line 64 as a comment and uncomment the 66th line 
#and run again the whole code after making the changes in lines 57 and 90 as described in comments near by        

#In order to obtain the financial-services news articles of daily FT News paper, make the line 64 as a comment and uncomment the 68th line 
#and run again the whole code after making the changes in lines 57 and 90 as described in comments near by 

#creating a dataframe          
df = pd.DataFrame(ft_news) 

#appending the website name to the dataframe
df['website_name'] = 'Daily FT'

#saving the obtained dataframe 'df' in the 'News Index' folder as a csv file

df.to_csv(r'E:\\News Index\\ft News_Business.csv')  
#The csv file name, 'ft News_Business.csv' in above line should be changed before running the code to extract entrepreneurship and financial-services news articles.
  
 