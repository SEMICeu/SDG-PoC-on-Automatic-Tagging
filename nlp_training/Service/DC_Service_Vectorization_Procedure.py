import pandas as pd
import os
import json
from pathlib import Path
import numpy as np

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#for model-building

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score
from joblib import dump, load

# bag of words

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#for word embedding

import gensim
from gensim.models import Word2Vec

dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_csv_path = str(dir_path.parent.absolute()) + "/data/html_data_translated_preprocessed.csv"

pandas_df=pd.read_csv(html_data_csv_path)

pandas_df = pandas_df.fillna("") # some nan in the data, to investigate

pandas_df_categorization = pd.DataFrame(pandas_df["clean_text"])
pandas_df_categorization["Information"] = [0]*len(pandas_df_categorization.index)
pandas_df_categorization["Procedure"] = [0]*len(pandas_df_categorization.index)

# print(pandas_df_categorization)
# print(pandas_df["metadata_type_string"])

for i in range(len(pandas_df_categorization.index)):
    if 'Information' in pandas_df.loc[i,"metadata_type_string"]:
        pandas_df_categorization.loc[i, "Information"] = 1

    if 'Procedure' in pandas_df.loc[i,"metadata_type_string"]:
        pandas_df_categorization.loc[i, "Procedure"] = 1

pandas_df_categorization = pandas_df_categorization.fillna("") # some nan in the data, to investigate
#SPLITTING THE TRAINING DATASET INTO TRAIN AND TEST
X_train, X_test, y_train, y_test = train_test_split(pandas_df_categorization["clean_text"],pandas_df_categorization["Procedure"],test_size=0.2,shuffle=True)

print(X_train)
print(y_train)
for i in X_train:
    if type(i) != str:
        print(i)
        print(type(i))



# Word2Vec runs on tokenized sentences
X_train_tok=[nltk.word_tokenize(i) for i in X_train]
X_test_tok=[nltk.word_tokenize(i) for i in X_test]

#building Word2Vec model
class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(next(iter(word2vec.values())))
    def fit(self, X, y):
            return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

pandas_df_categorization['clean_text_tok']=[nltk.word_tokenize(i) for i in pandas_df_categorization['clean_text']]
# model = Word2Vec(pandas_df_categorization['clean_text_tok'],min_count=1)
dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

print(dir_path)
# path_to_model = str(dir_path.parent.absolute()) + "/Service/Language_models/Word2Vec.model"
path_to_model = str(dir_path.parent.absolute()) + "/Service/Language_models/Word2Vec.model"
model = Word2Vec.load(path_to_model)
w2v = dict(zip(model.wv.index_to_key, model.wv.vectors))
modelw = MeanEmbeddingVectorizer(w2v)

# converting text to numerical data using Word2Vec
X_train_vectors_w2v = modelw.transform(X_train_tok)
X_test_vectors_w2v = modelw.transform(X_test_tok)

print(X_train_vectors_w2v)
print(X_test_vectors_w2v)

# FITTING THE CLASSIFICATION MODEL using Logistic Regression (W2v)
lr_w2v = LogisticRegression(solver='liblinear', C=10, penalty='l2')
lr_w2v.fit(X_train_vectors_w2v, y_train)  # model
# Predict y value for test dataset
y_predict = lr_w2v.predict(X_test_vectors_w2v)
y_prob = lr_w2v.predict_proba(X_test_vectors_w2v)[:, 1]
print(classification_report(y_test, y_predict))
print('Confusion Matrix:', confusion_matrix(y_test, y_predict))

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
print('AUC:', roc_auc)

# FITTING THE CLASSIFICATION MODEL random forest (W2v)
clf=RandomForestClassifier(n_estimators=100)
clf.fit(X_train_vectors_w2v, y_train)
# Predict y value for test dataset
y_predict = clf.predict(X_test_vectors_w2v)
y_prob = clf.predict_proba(X_test_vectors_w2v)[:, 1]
print(classification_report(y_test, y_predict))
print('Confusion Matrix:', confusion_matrix(y_test, y_predict))

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
print('AUC:', roc_auc)

dump(clf, 'Classification_models/DC_Service_Procedure_classification_model.joblib')