# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:36:12 2020

@author: Acer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
from wordcloud import WordCloud
import sklearn
#from sklearn import metrics
from tqdm import tqdm
from sklearn.svm import SVC
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics  import f1_score,accuracy_score
from sklearn.metrics import  confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV

loaded_df = pd.read_csv('cleaned_data.csv')
x_clean = loaded_df['Text'].tolist()
Y = loaded_df['Target'].tolist()

def models(x_clean, Y):

    
    df = pd.DataFrame(x_clean)
    df['Target']= Y
    df.columns = ['header','Target']
    
    
    for i in range(0,3):
        world = df.header[df.Target[df.Target==i].index] 
        plt.figure(figsize = (15,20))
        wordcloud = WordCloud(min_font_size = 3,  max_words = 2500 , width = 1200 , height = 800).generate(" ".join(world))
        plt.imshow(wordcloud,interpolation = 'bilinear');
        
    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(x_clean, Y, test_size = 0.3,random_state=42)

    train_x = np.array(X_train)
    test_x = np.array(X_test)
    train_y = np.array(Y_train)
    test_y = np.array(Y_test)


    tfidf_vect = TfidfVectorizer(min_df=1, strip_accents='unicode',token_pattern=r'\w{1,}', 
                                 ngram_range=(1, 3), use_idf=True,smooth_idf=True,sublinear_tf=True)

    # Fitting TF-IDF to both training and test sets
    tfidf_train = tfidf_vect.fit_transform(train_x)
    tfidf_test = tfidf_vect.transform(test_x)
    
    # Fitting BOW to both training and test sets 
    bow = sklearn.feature_extraction.text.CountVectorizer(analyzer = "word",max_features=5000)
    bow_train = bow.fit_transform(train_x)
    bow_test = bow.transform(test_x)
        
    
    # Logging for Visual Comparison
    log_cols=["Classifier", "Accuracy"]
    log = pd.DataFrame(columns=log_cols)
    
    # Fitting a simple Naive Bayes on TFIDF
    clf_MNB = MultinomialNB()
    clf_MNB.fit(tfidf_train, train_y)
    pred_MNB = clf_MNB.predict(tfidf_test)

    acc = metrics.accuracy_score(test_y, pred_MNB)
    
    log_entry = pd.DataFrame([['MultinomialNB', acc*100]], columns=log_cols)
    log = pd.concat([log, log_entry], ignore_index=True)
    
    # SVM
    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['linear'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
                   ]

    scores = ['precision']
    
    for score in scores:
        clf_tune = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                                scoring='%s_macro' % score)
        clf_tune.fit(tfidf_train, train_y)
        x = clf_tune.best_params_
        
    #Best SVM with 5 fold CV
    clf = SVC(kernel= x['kernel'], gamma = x['gamma'], C = x['C']) # rbf Kernel
    clf.fit(tfidf_train, train_y)
    pred_SVM = clf.predict(tfidf_test)
    acc = metrics.accuracy_score(test_y, pred_SVM)
    log_entry = pd.DataFrame([['SVM_rbf', acc*100]], columns=log_cols)
    log = pd.concat([log, log_entry], ignore_index=True)
    
    
    #KNN
    error = []

    # Calculating error for K values between 1 and 40
    for i in range(1,100):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(tfidf_train, train_y)
        pred_i = knn.predict(tfidf_test)
        error.append(np.mean(pred_i != test_y))
    
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, 100), error, color='red', linestyle='dashed', marker='o',
             markerfacecolor='blue', markersize=10)
    plt.title('Error Rate K Value with TFIDF')
    plt.xlabel('K Value')
    plt.ylabel('Mean Error')
    
    classifier = KNeighborsClassifier(n_neighbors=error.index(min(error)))
    classifier.fit(tfidf_train, train_y)

    y_pred = classifier.predict(tfidf_test)
    acc = metrics.accuracy_score(test_y, y_pred)
    log_entry = pd.DataFrame([['KNN', acc*100]], columns=log_cols)
    log = pd.concat([log, log_entry], ignore_index=True)
    
    
    ##Random forest
    
    ##Parameter tuning
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)] # Number of trees in random forest
    max_features = ['auto', 'sqrt'] # Number of features to consider at every split
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)] # Maximum number of levels in tree
    max_depth.append(None)
    min_samples_split = [2, 5, 10] # Minimum number of samples required to split a node
    min_samples_leaf = [1, 2, 4] # Minimum number of samples required at each leaf node
    bootstrap = [True, False] # Method of selecting samples for training each tree
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
    
    rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3,
                               verbose=2, random_state=42, n_jobs = -1)
    # Fit the random search model
    rf_random.fit(tfidf_train, train_y)

    y = rf_random.best_params_
    
    model = RandomForestClassifier(n_estimators=y['n_estimators'], 
                               bootstrap = y['bootstrap'],
                               max_features = y['max_features'], min_samples_split=y['min_samples_split'],
                               min_samples_leaf= y['min_samples_leaf'], max_depth = y['max_depth'])
    # Fit on training data
    model.fit(tfidf_train, train_y)
    rf_predictions = model.predict(tfidf_test)

    acc = metrics.accuracy_score(test_y, rf_predictions)
    log_entry = pd.DataFrame([['RandomForest', acc*100]], columns=log_cols)
    log = pd.concat([log, log_entry], ignore_index=True)

    ###################################################################################################    
    
     # Logging for Visual Comparison
    log_cols=["Classifier", "Accuracy"]
    log_bow = pd.DataFrame(columns=log_cols)
    
    # Fitting a simple Naive Bayes on TFIDF
    clf_MNB = MultinomialNB()
    clf_MNB.fit(bow_train, train_y)
    pred_MNB = clf_MNB.predict(bow_test)

    acc = metrics.accuracy_score(test_y, pred_MNB)
    
    log_entry = pd.DataFrame([['MultinomialNB', acc*100]], columns=log_cols)
    log_bow = pd.concat([log_bow, log_entry], ignore_index=True)

    
    # SVM
    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                    {'kernel': ['linear'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
                   ]

    scores = ['precision']
    
    for score in scores:
        clf_tune = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                                scoring='%s_macro' % score)
        clf_tune.fit(bow_train, train_y)
        x = clf_tune.best_params_
        
    #Best SVM with 5 fold CV
    clf = SVC(kernel= x['kernel'], gamma = x['gamma'], C = x['C']) # rbf Kernel
    clf.fit(bow_train, train_y)
    pred_SVM = clf.predict(bow_test)
    acc = metrics.accuracy_score(test_y, pred_SVM)
    log_entry = pd.DataFrame([['SVM_rbf', acc*100]], columns=log_cols)
    log_bow = pd.concat([log_bow, log_entry], ignore_index=True)

    
    
    #KNN
    error = []

    # Calculating error for K values between 1 and 40
    for i in range(1, 40):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(bow_train, train_y)
        pred_i = knn.predict(bow_test)
        error.append(np.mean(pred_i != test_y))
    
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
             markerfacecolor='blue', markersize=10)
    plt.title('Error Rate K Value with BOW')
    plt.xlabel('K Value')
    plt.ylabel('Mean Error')
    
    classifier = KNeighborsClassifier(n_neighbors=error.index(min(error)))
    classifier.fit(bow_train, train_y)

    y_pred = classifier.predict(bow_test)
    acc = metrics.accuracy_score(test_y, y_pred)
    log_entry = pd.DataFrame([['KNN', acc*100]], columns=log_cols)
    log_bow = pd.concat([log_bow, log_entry], ignore_index=True)

    
    
    ##Random forest
    
    ##Parameter tuning
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)] # Number of trees in random forest
    max_features = ['auto', 'sqrt'] # Number of features to consider at every split
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)] # Maximum number of levels in tree
    max_depth.append(None)
    min_samples_split = [2, 5, 10] # Minimum number of samples required to split a node
    min_samples_leaf = [1, 2, 4] # Minimum number of samples required at each leaf node
    bootstrap = [True, False] # Method of selecting samples for training each tree
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
    
    rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3,
                               verbose=2, random_state=42, n_jobs = -1)
    # Fit the random search model
    rf_random.fit(bow_train, train_y)

    y = rf_random.best_params_
    
    model = RandomForestClassifier(n_estimators=y['n_estimators'], 
                               bootstrap = y['bootstrap'],
                               max_features = y['max_features'], min_samples_split=y['min_samples_split'],
                               min_samples_leaf= y['min_samples_leaf'], max_depth = y['max_depth'])
    # Fit on training data
    model.fit(bow_train, train_y)
    rf_predictions = model.predict(bow_test)

    acc = metrics.accuracy_score(test_y, rf_predictions)
    log_entry = pd.DataFrame([['RandomForest', acc*100]], columns=log_cols)
    log_bow = pd.concat([log_bow, log_entry], ignore_index=True)

    
    log['method'] = 'TFIDF'
    log_bow['method'] = 'BOW'
    final= pd.concat([log_bow,log], ignore_index = True)
    
    return final
    
  
final_df = models(x_clean , Y)




# set width of bar
barWidth = 0.25
 
# set height of bar
bars1 = final_df[final_df['method']=='BOW']['Accuracy']
bars2 = final_df[final_df['method']=='TFIDF']['Accuracy']

 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]

 
# Make the plot
plt.bar(r1, bars1, color='#313554', width=barWidth, edgecolor='white', label='BOW')
plt.bar(r2, bars2, color='#19a698', width=barWidth, edgecolor='white', label='TFIDF')

 
# Add xticks on the middle of the group bars
plt.xlabel('Classifier', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(bars1))], ['Multinomial NB', 'SVM_rbf', 'KNN', 'Random Forest'])
 
# Create legend & Show graphic
plt.ylabel('Accuracy %', fontweight='bold')
plt.title('Classifier Accuracy')
plt.legend(bbox_to_anchor=(1, 1.05),
           bbox_transform=plt.gcf().transFigure)
plt.show()
    