# NLPforFinancialNews
A machine learning-based news recommendation engine for financial analysts, using web scraping, NLP techniques, and deep learning models to efficiently recommend relevant news articles.

## Overview:
Referring to news articles is a critical activity for financial analysts, as it enables the extraction of accurate financial insights. However, the vast volume of news articles generated daily makes identifying relevant content a time-consuming and challenging task. This project develops a modeling framework for an intelligent news recommendation engine tailored for financial analysts. The framework efficiently recommends the most relevant articles based on analysts' preferences, eliminating the need for tedious manual browsing.

This project is part of my BSc final-year research conducted in 2020, with additional modifications and updates made in 2025. 

## Tools and Libraries Used:
Web Scraping: BeautifulSoup, Requests

NLP: NLTK, Tokenization, Stopword Removal, Stemming, Lemmatization

Machine Learning: Scikit-learn

Deep Learning: Keras, TensorFlow (LSTM, CNN)


## Core Components of the Project:

1. Data Collection via Web Scraping:

  News articles were retrieved from various online news platforms using advanced web scraping techniques.
  Libraries like BeautifulSoup and Requests were employed to automate the extraction of article text, metadata, and timestamps, ensuring a rich dataset for analysis.

2. Analyst Preferences Data:

  A response variable representing analysts' preferences for each article was manually acquired from a group of financial analysts at a selected financial company.
  This data served as the labeled dataset for the recommendation engine.

3. Natural Language Processing (NLP):

  Text preprocessing was performed using techniques such as:
    Tokenization
    Stopword removal
    Stemming and lemmatization
    The synonym replacement method was employed as a text data augmentation technique to address class imbalance in the dataset.

4. Machine Learning and Deep Learning Models:

  A classification-based method was adopted to build the recommendation engine.
  Models experimented with included:
    Machine Learning Models: K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Random Forest.
    Deep Learning Models: Long Short-Term Memory (LSTM), Convolutional Neural Networks (CNN).
    CNN achieved the highest accuracy, outperforming the other approaches and was chosen as the most suitable model for this task.

5. Performance Insights:

  The study revealed that deep learning models demonstrated significantly better performance compared to traditional machine learning techniques in the context of news recommendation engines.
  The developed framework is modular and can be adapted for use by other financial companies or domains with similar needs.


## Publication Details:
The methodology, findings, and further insights from this study are documented in the research paper. You can read the full publication here: https://icter.sljol.info/articles/10.4038/icter.v16i4.7269.
