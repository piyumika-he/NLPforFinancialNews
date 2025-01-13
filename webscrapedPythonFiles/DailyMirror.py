# -*- coding: utf-8 -*-

#importing libraries 
import pandas as pd    
from selenium import webdriver
import time

#path where the chromedriver.exe file is saved
Path = 'C:\Program Files (x86)\chromedriver.exe'

#automatically opening the web page of the given url in google chrome 
driver = webdriver.Chrome(Path)
driver.get('http://www.dailymirror.lk/archives')

#stopping the proramme for 5 seconds until the given page load
time.sleep(5)


#######################
# To run until the end. As there's no need to extract news items from the begining, this section is kept as a comment.
# click_more = True
# while click_more:
#     time.sleep(2)
#     element = driver.find_element_by_xpath('/html/body/header/span/div/div/div[1]/header/div/div[2]/nav/ul/li[7]/span')
#     print(i)
#     i=i+1
#     if element:
#         element.click()
#     else:
#         click_more = False  
######################

#the value assigns to 'page_no' variable should be changed accordingly. The number of pages where the required articles are in, have to be assigned to the variable
page_no = 5
i=1

#creating the new variable news
news =[]

for i in range (1,page_no):

    #seperate only the section where the required news articles can be found
    main = driver.find_element_by_class_name('top-header-sub')

    #obtaining each news article seperately
    articleList = main.find_elements_by_class_name('col-md-8')
    len(articleList)
    
    #for loop to extract required variables
    for article in articleList:
        news_dict ={}
        #obtaining header
        news_dict['header']= article.find_element_by_tag_name('h3').text
        
        #obtaining content under p tag
        p_tags = article.find_elements_by_tag_name('p')
        
        #obtaiining the date
        date = p_tags[0].text
        news_dict['date']=date
        
        #obtaining the content of the article
        news_dict['body']=p_tags[1].text
        
        #appending extracted varibles of each news article into 'news' variable 
        news.append(news_dict)
    #Automatically loading the next page   
    loadMoreButton = driver.find_element_by_xpath('/html/body/header/span/div/div/div[1]/header/div/div[2]/nav/ul/li[7]/span')
    loadMoreButton.click()
    time.sleep(5)
    print(i)
    
#creating a dataframe        
df = pd.DataFrame(news) 

#appending the website name to the dataframe
df['website_name'] = 'Daily Mirror'

#saving the obtained dataframe 'df' in the 'News Index' folder as a csv file
df.to_csv(r'E:\\News Index\\Daily Mirror.csv') 