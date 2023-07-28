# -*- coding: utf-8 -*-
"""Sephora_Recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bs0W85BneICU54eOSHn0FVuAscnVjKpK
"""

# Sklearn and Pandas Setup
import json
import glob
import pandas as pd
import numpy as np
import datetime as dt
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from google.colab import drive
from sklearn.model_selection import train_test_split

products_df = pd.concat(map(pd.read_csv, ['cheek_products.csv', 'concealer_products.csv',
                                          'eyebrow_products.csv', 'eyeliner_products.csv',
                                          'eyeshadow_products.csv', 'foundation_products.csv',
                                          'lip_products.csv', 'mascara_products.csv',
                                          'powder_products.csv', 'primer_products.csv']))
# products_df = products_df.drop(columns=['Unnamed:0'])
products_df

products_df.columns

# drop product id, brand id, value price, sale price, limited edition, new, online only, out of stock, sephora exclusive, child max price, child min price
products_df = products_df.drop(columns=['Unnamed: 0'])
products_df.head(2)

products_df.columns

"""# Data Cleaning"""

categories = products_df['category'].unique().tolist()
categories

len(products_df)

products_df = products_df.loc[products_df['category'] != 'Makeup']
products_df = products_df.loc[products_df['category'] != 'Mini Size']
products_df = products_df.loc[products_df['category'] != 'Value & Gift Sets']
products_df = products_df.loc[products_df['category'] != 'Category Unavailable']
products_df = products_df.loc[products_df['category'] != 'Mists & Essences']
len(products_df)

categories = products_df['category'].unique().tolist()
categories

def main_cat(input):
  if ((input == 'Blush') | (input == 'Bronzer') | (input == 'Contour') | (input == 'Cheek Palettes') | (input == 'Highlighter')):
    return 'Cheek'
  elif ((input == 'Face Serums') | (input == 'Setting Spray & Powder') | (input == 'Concealer') | (input == 'Foundation') | (input == 'Tinted Moisturizer') | (input == 'BB & CC Cream') | (input == 'Face Sunscreen') | (input == 'Face Primer') | (input == 'Moisturizers') | (input == 'Face Sets')):
    return 'Face'
  elif ((input == 'Lip Stain') | (input == 'Liquid Lipstick') | (input == 'Lip Liner') | (input == 'Lipstick') | (input == 'Lip Balms & Treatments') | (input == 'Lip Gloss') | (input == 'Lip Plumper') | (input == 'Lip Sets')):
    return 'Lip'
  elif ((input == 'Under-Eye Concealer') | (input == 'Eye Creams & Treatments') | (input == 'Eyebrow') | (input == 'Mascara') | (input == 'Eye Brushes') | (input == 'Eye Sets') | (input == 'Tweezers & Eyebrow Tools') | (input == 'Eye Palettes')):
    return 'Eye'
  else:
    return 'n/a'

products_df['general_cat'] = products_df['category'].apply(main_cat)
products_df

products_df = products_df[products_df['general_cat'] != 'n/a']
products_df = products_df[products_df['price'] != 'Price not available']
products_df = products_df[products_df['number_of_reviews'] != 'Review count not available']
len(products_df)

products_df.info()

def let_user_pick(options):
    print("What type of product are you looking for today?\n")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None

options = products_df['general_cat'].unique().tolist()
res = let_user_pick(options)
cat1 = options[res]
print(options[res])

cat1_df = products_df[products_df.general_cat == cat1].reset_index()
cat1_df = cat1_df.drop(columns=['index'])
# cat1_df = cat1_df.dropna(subset=['secondary_category'])
cat1_df.head(5)

options = cat1_df['category'].unique()
print(options)

def let_user_pick(options):
    print("What type of product are you looking for within the " + cat1 + " category?\n")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None

options = cat1_df['category'].unique().tolist()
res2 = let_user_pick(options)
cat2 = options[res2]
print(options[res2])

cat2_df = cat1_df[cat1_df.category == cat2].reset_index()
cat2_df = cat2_df.drop(columns=['index'])
cat2_df.head(5)

min, max = cat2_df['price'].agg(['min', 'max'])
print(min)
print(max)

def convert(x):
  x = x.strip('$')
  return round(float(x))

cat2_df['price_usd'] = cat2_df['price'].apply(convert)
cat2_df.head(5)

qlist = cat2_df['price_usd'].quantile([0.25, 0.5, 0.75]).tolist()

qlist_int = [round(q) for q in qlist]
print(qlist_int)

def let_user_pick(options):
    print("Do you have a price range in mind?\n")

    for idx, element in enumerate(options):
      if idx == len(options) - 1:
        print("{}) Any price range".format(idx + 1))
      else:
        print("{}) Up to ${}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None

options = qlist_int
options.append('Any of the above')
p_res = let_user_pick(options)
p_op = options[p_res]
print(options[p_res])

if p_op == 'Any price range':
  price_df = cat2_df
else:
  price_df = cat2_df[cat2_df.price_usd <= p_op]

price_df

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
stopwords = set(stopwords.words('english'))

def tokenize_content(content):
  tk_list = nltk.word_tokenize(content)

  tk_list_3 = list()
  for x in tk_list:
    if x.isalpha():
      tk_list_3.append(x)
  tk_list_2 = map(lambda x : x.lower(), tk_list_3)
  final_tk = [item for item in tk_list_2 if item not in stopwords]

  return final_tk

price_df['tokenized'] = price_df['reviews'].apply(lambda x : tokenize_content(x))
price_df

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def retrieve_sentiment(content):
  return sia.polarity_scores(content)

price_df['sentiment'] = price_df['reviews'].apply(lambda x : retrieve_sentiment(x).get('compound'))

price_df = price_df.sort_values(by = ['sentiment'], ascending=False)
price_df

price_df = price_df.sort_values(by=['like_count', 'rating', 'sentiment'], ascending=[False, False, False])
price_df

price_df.head(3)