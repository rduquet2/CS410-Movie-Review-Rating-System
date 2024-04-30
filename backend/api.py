from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

import numpy as np
import csv
from nltk.corpus import stopwords
from collections import Counter
import re

app = Flask(__name__)

def get_reviews(movie):
   page = 'https://www.imdb.com/'
   driver = webdriver.Chrome()
   driver.get(page)
   search_form = driver.find_element(By.ID, "suggestion-search")
   search_form.send_keys(movie)
   search_button = driver.find_element(By.ID, "suggestion-search-button")
   search_button.click()
   time.sleep(5)
   movie_link = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")[0]
   movie_link.click()
   time.sleep(5)
   reviews_link = driver.find_element(By.LINK_TEXT, "User reviews")
   reviews_link.click()
   time.sleep(5)
   dropdown = Select(driver.find_element(By.CLASS_NAME, "lister-sort-by"))
   dropdown.select_by_index(1)
   time.sleep(5)
   reviews = driver.find_elements(By.CSS_SELECTOR, "div[class^='text show-more__control']")
   reviews_text = [review.text for review in reviews]
   recent_reviews = reviews_text[:20]
   return recent_reviews

def train_model(train):
   # CREATE FREQUENCY TABLE
   frequencies = dict()
   for class_name, texts in train.items():
       bigram_tokens = []
       for text in texts:
           for i in range(len(text)-1):
               bigram_tokens.append(text[i] + " " + text[i+1])
       frequencies[class_name] = Counter(bigram_tokens)

   # REMOVE STOPWORDS FROM TABLE
   stop_words = set(stopwords.words('english'))
   cleaned_frequencies = {}
   for class_name, counts in frequencies.items():
       cleaned_frequencies[class_name] = Counter()
       for bigram, count in counts.items():
           token_pair = bigram.split(" ")
           if (token_pair[0] not in stop_words or token_pair[1] not in stop_words):
               cleaned_frequencies[class_name][bigram] = count

   # SMOOTH THE FREQUENCIES USING LAPLACE
   smoothing_constant = 0.01
   likelihood = {}
   for class_name, counts in cleaned_frequencies.items():
       likelihood[class_name] = {}
       count_total = sum(counts.values())
       for bigram, count in counts.items():
           likelihood[class_name][bigram] = (count+smoothing_constant)/(count_total + (smoothing_constant*(len(counts)+1)))
       likelihood[class_name]['OOV'] = smoothing_constant/(count_total + (smoothing_constant*(len(counts)+1)))
   return likelihood

# CLASSIFY A REVIEW
def classify(text, likelihood, prior):
   text = text.split()
   pos_total = np.log(prior)
   neg_total = np.log(1-prior)
   stop_words = set(stopwords.words('english'))
   for k in range(len(text)-1):
       if (text[k] not in stop_words or text[k+1] not in stop_words):
           if ((text[k] + " " + text[k+1]) in likelihood["positive"]):
               pos_total += np.log(likelihood["positive"][text[k] + " " + text[k+1]])
           else:
               pos_total += np.log(likelihood["positive"]["OOV"])
           if ((text[k] + " " + text[k+1]) in likelihood["negative"]):
               neg_total += np.log(likelihood["negative"][text[k] + " " + text[k+1]])
           else:
               neg_total += np.log(likelihood["negative"]["OOV"])
   if (pos_total > neg_total):
       return ("Positive", pos_total, neg_total)
   else:
       return ("Negative", pos_total, neg_total)

@app.route('/getTitle', methods=['GET', 'POST'])
def submit_form():
   data = request.json
   movie = data['title']
   reviews = get_reviews(movie)
   print(reviews)
   
   training_data = dict()
   training_data['positive'] = []
   training_data['negative'] = []
   with open('TrainingData.csv', newline='', encoding='utf-8') as csvfile:
       reader = csv.reader(csvfile)
       next(reader)
       for review_sentiment in reader:
           review = review_sentiment[0]
           review = review.lower()
           review = re.sub(r'[^a-z\s]', '', review)
           review = re.sub(r'\s+', ' ', review)
           review = review.split()
           sentiment = review_sentiment[1]
           training_data[sentiment].append(review)

   likelihood = train_model(training_data)

   pos_count = 0
   neg_count = 0
   for r1 in reviews:
       if (classify(r1, likelihood, prior = 0.8)[0] == "Positive"):
           pos_count += 1
       else:
           neg_count += 1
   if (pos_count/(pos_count+neg_count) >= 0.85):
       return jsonify({'message': ["We recommend this movie!", 'Approximately {(pos_count/(20)) * 100}% of this movie\'s reviews had positive sentiment']})

   return jsonify({'message': ["We do not recommend this movie", 'Approximately {(pos_count/(20)) * 100}% of this movie\'s reviews had positive sentiment']})
   


if __name__ == '__main__':
   app.run(debug=True)
