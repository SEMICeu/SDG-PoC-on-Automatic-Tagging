import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
import seaborn as sns

#for text pre-processing

import re, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

#for model-building

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score

# bag of words

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#for word embedding

import gensim
from gensim.models import Word2Vec

dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_tagged_json_path = str(dir_path.parent.absolute()) + "/data/html_data.json"

with open(html_data_tagged_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['html_list']

pandas_df = pd.DataFrame(data)
print(pandas_df.info())

x=pandas_df['metadata_type_string'].value_counts()
print(x)



# remove space and other non wanted character
def first_clean(text):
    return " ".join(text.split())
# convert to lowercase, strip and remove punctuations
def preprocess(text):
    text = text.lower()
    text = text.strip()
    text = re.compile('<.*?>').sub('', text)
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# STOPWORD REMOVAL
def stopword(string):
    a = [i for i in string.split() if i not in stopwords.words('english')]
    return ' '.join(a)


# LEMMATIZATION
# Initialize the lemmatizer
wl = WordNetLemmatizer()


# This is a helper function to map NTLK position tags
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# Tokenize the sentence
def lemmatizer(string):
    word_pos_tags = nltk.pos_tag(word_tokenize(string))  # Get position tags
    a = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for idx, tag in
         enumerate(word_pos_tags)]  # Map the position tag and lemmatize the word/token
    return " ".join(a)


def finalpreprocess(string):
    global n
    n= n+1
    print("**************")
    print("n is : ")
    print(n)
    print("length of the text is : ")
    print(len(first_clean(string)))
    return lemmatizer(stopword(preprocess(first_clean(string))))

n=0
print("begin pre-processing")
pandas_df['clean_text'] = pandas_df['html'].apply(lambda x: finalpreprocess(x))
print("end pre-processing")
pandas_df.head()

pandas_df.to_csv(path_or_buf=str(dir_path.parent.absolute()) + "/data/html_data_preprocessed.csv", index=False)

pandas_df_categorization = pd.DataFrame(pandas_df["clean_text"])
pandas_df_categorization["Information"] = [0]*len(pandas_df_categorization.index)
pandas_df_categorization["Procedure"] = [0]*len(pandas_df_categorization.index)

print(pandas_df_categorization)

for i in range(len(pandas_df_categorization.index)):
    if 'Information' in pandas_df.loc[i,"metadata_type_string"]:
        pandas_df_categorization.loc[i, "Information"] = 1

    if 'Procedure' in pandas_df.loc[i,"metadata_type_string"]:
        pandas_df_categorization.loc[i, "Procedure"] = 1

#SPLITTING THE TRAINING DATASET INTO TRAIN AND TEST
X_train, X_test, y_train, y_test = train_test_split(pandas_df_categorization["clean_text"],pandas_df_categorization["Information"],test_size=0.2,shuffle=True)

# Word2Vec runs on tokenized sentences
X_train_tok=[nltk.word_tokenize(i) for i in X_train]
X_test_tok=[nltk.word_tokenize(i) for i in X_test]