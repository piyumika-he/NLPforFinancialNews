# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 07:51:14 2020

@author: Acer
"""


import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
import string
pd.options.mode.chained_assignment = None
nltk.download('stopwords')
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
from wordcloud import WordCloud
import sklearn
from sklearn import metrics
#for lemmatization
from nltk.corpus import wordnet
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')
import matplotlib.ticker as ticker
from nltk.stem import PorterStemmer
nltk.download('gutenberg')



df = pd.read_csv('C:\\Users\\piyum\\Documents\\Analysis\\final.csv')
df.head()

########################################################################################################
#barplot response with 11 categories
total = len(df)*1.
plt.figure(figsize=(12,8))
sns.set(font_scale=1.5)
ax = sns.countplot(x="Rate", data=df)
plt.title('Distribution of Response variable')
plt.xlabel('Response')
plt.ylabel('Frequency [%]')

for p in ax.patches:
        ax.annotate('{:.1f}%'.format(100*p.get_height()/total), (p.get_x()+0.1, p.get_height()+5))

#put 11 ticks (therefore 10 steps), from 0 to the total number of rows in the dataframe
ax.yaxis.set_ticks(np.linspace(0, total, 11))

#adjust the ticklabel to the desired format, without changing the position of the ticks. 
_ = ax.set_yticklabels(map('{:.1f}%'.format, 100*ax.yaxis.get_majorticklocs()/total))

plt.show()
###########################################################################################################


#model with titles
X = df["Title"]
Y = df["Rate"]

#model with body content
X = df["Body"]
Y = df["Rate"]

#with clustered response
Relevency = []
for i in range(0,len(df)):
    if df['Rate'][i]>6:
        x= 0
    elif df['Rate'][i]>3 :
        x = 1
    else:
        x=2
    Relevency.append(x)

df['Response'] = Relevency

X = df["Body"]
Y = df["Response"]

#############

df["new"] = df["Body"] + df["Website"] + df['Title'] + df['Keywords']

X = df["new"]
Y = df["Response"]

########################################################################################################
#barplot response
total = len(df)*1.
plt.figure(figsize=(12,8))
sns.set(font_scale=2)
ax = sns.countplot(x="Response", data=df, palette="mako" )
plt.title('Distribution of Response variable')
plt.xlabel('Response')
plt.ylabel('Frequency [%]')

for p in ax.patches:
        ax.annotate('{:.1f}%'.format(100*p.get_height()/total), (p.get_x()+0.1, p.get_height()+5))

#put 11 ticks (therefore 10 steps), from 0 to the total number of rows in the dataframe
ax.yaxis.set_ticks(np.linspace(0, total, 11))

#adjust the ticklabel to the desired format, without changing the position of the ticks. 
_ = ax.set_yticklabels(map('{:.1f}%'.format, 100*ax.yaxis.get_majorticklocs()/total))

plt.show()

###########################################################################################################

#pie chart

x = 0
y=0
z=0

for i in range(0,len(df)):
    if Relevency[i]==2:
        x = x+1
    elif Relevency[i]==1:
        y=y+1
    else:
        z=z+1

count = (x,y,z)

activities = ['Low Relevance', 'Middle relevance','High relevance']

plt.pie(count, labels=activities, startangle=90, autopct='%.1f%%')

plt.show()

#########################################################################################################

##website wise relevnt articles

label = []
for i in range(0,len(df)):
    if df['Response'][i]==0:
        x= "High relevance"
    elif df['Response'][i]==1 :
        x = "Middle relevance"
    else:
        x="Low relevance"
    label.append(x)

df['label'] = label

sns.set(font_scale=1)
ax = sns.countplot(x="Website", hue="label", data=df, saturation=1,palette="mako",hue_order=("High relevance","Middle relevance","Low relevance"))
plt.show()

####################################################################################################33
total = len(df)*1.
plt.figure(figsize=(12,8))
sns.set(font_scale=2)
ax = sns.countplot(x="Website", data=df, palette="mako", order=('Engadget','BBC','The Verge','Tech2','Reuters','Mashable'))
plt.title('Number of marked articles of each website')
plt.xlabel('Website Name')
plt.ylabel('Count')

for p in ax.patches:
        ax.annotate(format(p.get_height()), (p.get_x()+0.1, p.get_height()+5))

plt.show()
###################################################################################################



lemmatizer = WordNetLemmatizer()
wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    
    ##Data preprocessing
def get_words( headlines ):               
    text_onlyletters = re.sub("[^a-zA-Z]", " ",headlines) #Remove everything other than letters     
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    without_urls = url_pattern.sub(r'', text_onlyletters)
    html_pattern = re.compile('<.*?>')
    without_htmltags = html_pattern.sub(r'', without_urls)
    words = without_htmltags.lower().split() #Convert to lower case, split into individual words    
    stops = set(stopwords.words("english"))  #Convert the stopwords to a set for improvised performance                 
    meaningful_words = [w for w in words if not w in stops]   #Removing stopwords
    remove_oneletter = [w for w in meaningful_words if len(w)>2]
    stemmer = PorterStemmer()
    stemming = [stemmer.stem(word) for word in remove_oneletter]
    pos_tagged_text = nltk.pos_tag(stemming) #lemmatization
    return " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text]) #Joining the words


x_clean = []
for i in range(0,len(X)):
    print(i)
    cleanHeadline = get_words(X[i]) #Processing the data and getting words with no special characters, numbers or html tags and with root words
    x_clean.append(cleanHeadline) 



#############################################################

df = pd.DataFrame(x_clean)
df['Target']= Y
df.columns = ['header','Target']

middle = df.header[df.Target[df.Target==1].index]
good = df.header[df.Target[df.Target==0].index]
bad = df.header[df.Target[df.Target==2].index]
spliteData = [good,middle,bad]
color = ['Accent','Paired','hot']
for item in range(3):
    plt.figure(figsize=(30,10))
    plt.rcParams.update({'font.size': 50})
    pd.Series(''.join([i for i in spliteData[item]]).split()).value_counts(normalize=True).head(20).plot(kind='bar',colormap=color[item])
    plt.show()
    
#As we can observe below words are appearing many times in each category we remove them    

def word_remove_say(xy):
    return ' '.join([i for i in xy.split() if i != 'say'])

def word_remove_company(xy):
    return ' '.join([i for i in xy.split() if i != 'company'])

def word_remove_also(xy):
    return ' '.join([i for i in xy.split() if i != 'also'])

def word_remove_new(xy):
    return ' '.join([i for i in xy.split() if i != 'new'])
def word_remove_make(xy):
    return ' '.join([i for i in xy.split() if i != 'make'])
def word_remove_year(xy):
    return ' '.join([i for i in xy.split() if i != 'year'])
def word_remove_get(xy):
    return ' '.join([i for i in xy.split() if i != 'get'])
def word_remove_would(xy):
    return ' '.join([i for i in xy.split() if i != 'would'])
def word_remove_use(xy):
    return ' '.join([i for i in xy.split() if i != 'use'])
def word_remove_app(xy):
    return ' '.join([i for i in xy.split() if i != 'app'])


final_vector = []
for i in range(0,len(X)):
    x = word_remove_say(x_clean[i]) #Processing the data and getting words with no special characters, numbers or html tags and with root words
    y = word_remove_company(x)
    z = word_remove_also(y)
    a = word_remove_new(z)
    b = word_remove_make(a)
    c = word_remove_year(b)
    d = word_remove_get(c)
    e = word_remove_would(d)
    f = word_remove_app(e)
    final = word_remove_use(f)
    
    final_vector.append(final) 


x_clean = final_vector

save_df = pd.DataFrame({'Text': x_clean, 'Target': Y})

save_df.to_csv('C:\\Users\\piyum\\Documents\\Analysis\\cleaned_data.csv', index=False)









    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
