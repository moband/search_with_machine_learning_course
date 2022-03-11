import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

from cleantext import clean

from sklearn.utils import shuffle
from sklearn.model_selection import StratifiedShuffleSplit

# Useful if you want to perform stemming.
import nltk

def stratify_dataframe(df, label_column = "label", split_size = 50000) :
    num_datapoints = df.shape[0]
    n_splits = int(num_datapoints / split_size)

    sss = StratifiedShuffleSplit(n_splits=n_splits, train_size=split_size, test_size=split_size, random_state=4711)
    train_index, test_index = list(sss.split(df, df[label_column]))[0]
    return df.iloc[train_index], df.iloc[test_index]

def get_parent(child_cat):
    return child_cat if child_cat==root_category_id else parents_df[parents_df['category']  == child_cat]['parent'].values[0]

def apply_cut_off(dataset, cut_off):
    dataset['cat_size'] = dataset.groupby('category')['query'].transform('count')
    condition = lambda cutoff : dataset['cat_size'] < cutoff

    while len(dataset[condition(cut_off)]):
        dataset.loc[condition(cut_off), ['category']]=dataset.loc[condition(cut_off),['category']].applymap(lambda cat: get_parent(cat))
        dataset['cat_size'] = dataset.groupby('category')['query'].transform('count')
    
    return dataset

def clean_text(q):
    q = clean(q, lower=True,no_punct=True, no_line_breaks=True, no_numbers=True,no_currency_symbols=True)
    return " ".join([stemmer.stem(token) for token in q.split()])

stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/100/labeled_query_data.txt'
train_file_name = r'/workspace/datasets/100/train.data'
test_file_name = r'/workspace/datasets/100/test.data'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])
parents_df.set_index('category')
# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]
df=df.sample(500000)

# clean text queries
print('cleaning text queries ...')
df['query'] = df['query'].apply(lambda q: clean_text(q))

# apply cut off criteria 
print('applying cut off criteria ...')
df = apply_cut_off(df, cut_off=min_queries)

print(f'dataset size {len(df)}')
print(f'number of unique categories in complete dataset: {df["category"].nunique()}')

# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']

train_data, test_data = stratify_dataframe(df)
print(f'number of unique categories in train dataset: {train_data["category"].nunique()}')
print(f'number of unique categories in test dataset: {test_data["category"].nunique()}')

print('saving dataset ...')
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
train_data[['output']].to_csv(train_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
test_data[['output']].to_csv(test_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
