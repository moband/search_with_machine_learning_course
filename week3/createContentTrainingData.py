import argparse
import os
import re
import string
import unicodedata
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from nltk.stem import SnowballStemmer
from nltk.tokenize import casual_tokenize

from sklearn.utils import shuffle

import numpy as np
import pandas as pd

def stem_text(text):
    stemmed_words = []
    for word in casual_tokenize(text):

        stemmed_word = snowball.stem(word.strip())
        stemmed_words.append(stemmed_word)

    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text

def normalize_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_punctuation(text):
    return str(text).translate(str.maketrans('', '', string.punctuation))

def transform_name(product_name):
    product_name = product_name.lower().strip()
    product_name = re.sub(r'[\r|\n|\r\n]+', ' ',product_name)
    product_name = remove_punctuation(product_name)
    product_name = normalize_accented_chars(product_name)
    product_name = stem_text(product_name)

    return product_name

def save_infrequent_labels_report(file, df):
    infrequent_labels =  (dataset_df.groupby('label')
                                    .filter(lambda x : len(x) <= min_products))

    infrequent_labels_counts = (infrequent_labels
                                    .groupby('label')
                                    .size()
                                    .sort_values(ascending=False)
                                    .reset_index(name='count'))

    infrequent_labels_counts.to_csv(file, index=False, header=True)

    print(f'{len(infrequent_labels_counts)} infrequent labels will be eliminated from dataset.')

# Directory for product data
directory = r'/workspace/search_with_machine_learning_course/week3/pruned_products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")
general.add_argument("--min_products_report", default="/workspace/datasets/fasttext/min_products_report.csv",  help="The file to output infrequent product labels.")

# Consuming all of the product data will take over an hour! But we still want to be able to obtain a representative sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

# IMPLEMENT: Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

general.add_argument("--cat_granularity_level", default=0, type=int, help="granularity level of choosing a product category (i.e. Number of backward steps from the leaf depth).")


general.add_argument("--train_num_obs", default=10000,  help="Number of observations in the train file.")
general.add_argument("--test_num_obs", default=10000,  help="Number of observations in the test file.")

snowball = SnowballStemmer(language='english')

args = parser.parse_args()
output_file = args.output
path = Path(output_file)

output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

# set train, test and infrequent labels report files
test_file = os.path.abspath(os.path.join(output_dir, 'test.data'))
train_file = os.path.abspath(os.path.join(output_dir, 'train.data'))
infrequent_labels_report_file = os.path.abspath(os.path.join(output_dir, 'infrequent_labels.report'))

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products

sample_rate = args.sample_rate

train_num_obs = int(args.train_num_obs)
test_num_obs = int(args.test_num_obs)

cat_granularity_level  = args.cat_granularity_level

data_rows = []
print("Writing results to %s" % output_file)

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        print("Processing %s" % filename)
        f = os.path.join(directory, filename)
        tree = ET.parse(f)
        root = tree.getroot()
        for child in root:
            if random.random() > sample_rate:
                continue
            # Check to make sure category name is valid
            if (child.find('name') is not None and child.find('name').text is not None and
                child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
                child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None):
                    # Choose element in categoryPath corresponding to granularity level.
                    num_sub_cats = len(child.find('categoryPath'))
                    depth_at_ancestor = min(([num_sub_cats - i for i in range(cat_granularity_level + 1) if num_sub_cats - i >= 0]))

                    cat = child.find('categoryPath')[depth_at_ancestor - 1][0].text
                    # Replace newline chars with spaces so fastText doesn't complain
                    name = child.find('name').text.replace('\n', ' ')
                    label = "__label__%s" % cat
                    name = transform_name(name)
                    data_rows.append(dict([('label', label),('name', name)]))

dataset_df = pd.DataFrame(data_rows)

#report infrequent labels with counts
if min_products > 0:
    save_infrequent_labels_report(infrequent_labels_report_file, dataset_df)

#filter data to include frequent product lables that matches the criteria
dataset_df = dataset_df.groupby('label').filter(lambda x : len(x) > min_products)

#shuffle dataset
dataset_df = shuffle(dataset_df)

#prepare train and test datasets
train_data = dataset_df[:train_num_obs]
test_data = dataset_df[-1 * test_num_obs:]

#save the whole dataset with splitted test and train data 
print(f'saving {len(train_data)} observations in the train file : {train_file} ')
np.savetxt(train_file, train_data.values, fmt = "%s")

print(f'saving {len(test_data)} observations in the test file : {test_file} ')
np.savetxt(test_file, test_data.values, fmt = "%s")

print(f'saving {len(dataset_df)} as complete dataset : {output_file} ')
np.savetxt(output_file, dataset_df.values, fmt = "%s")


