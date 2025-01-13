# -*- coding: utf-8 -*-

#importing libraries
import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd   
from selenium import webdriver
import time

#path where the chromedriver.exe file is saved
Path = 'C:\Program Files (x86)\chromedriver.exe'

#opening the web page of the given url in google chrome automatically
driver = webdriver.Chrome(Path)
#obtaining news items in ft section of ceylon today news paper
driver.get('https://ceylontoday.lk/category/print-edition/ft')


#stopping the proramme for 5 seconds until the given page load
time.sleep(5)

#creating the new variable news
news =[] 

#There are altogether 54 pages where we can find the previous ft news.
#The value of the variable 'no' should be changed accordingly Ex: In order to extract all the news in the business section 'no' should be given as 3  
no = 55
for i in range (1,no):
    
    
    print(i)
    #seperate only the section where the required news articles are in.
    main = driver.find_element_by_class_name('news-container')

    #obtaining each news article seperately
    articleList = main.find_elements_by_tag_name('div.col-md-4')
    len(articleList)
    
    #for loop to extract required variables
    for article in articleList:
        news_dict ={}
        #obtaining header
        news_dict['header']= article.find_element_by_tag_name('h3').text
        #obtaining date
        news_dict['date']= article.find_element_by_tag_name('div.news-date').text
        #obtaining url for the web page where we can find the full content of the article
        url = article.find_element_by_tag_name("a").get_attribute('href')
        news_dict['url'] = url  
    
        #Going inside to that extracted url
        response_url = requests.get(url)
        soup_url = bs(response_url.text)
    
        #obtaining the full content of the article
        x = soup_url.select('div.news-content p')
        para = ''.join([element.text for element in x])
    
        news_dict['body']=para
        

        #appending extracted varibles of each news article into 'news' variable 
        news.append(news_dict)
    #Automatically loading the next page
    loadMoreButton = driver.find_element_by_xpath('//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[1]/div/div[2]/nav/ul/li[10]/a')
    loadMoreButton.click()
    #stopping the proramme for 5 seconds until the given page load
    time.sleep(5)

        
    
#creating a dataframe      
df = pd.DataFrame(news) 

#appending the website name to the dataframe
df['website_name'] = 'Ceylon Today'

#saving the obtained dataframe 'df' in the 'News Index' folder as a csv file

df.to_csv(r'E:\\News Index\\Ceylon_ft.csv') 

