import pandas as pd
import os
import json
from pathlib import Path
import numpy as np
import pickle

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

# for classification
from skmultilearn.adapt import MLkNN, MLTSVM, BRkNNaClassifier
from sklearn.metrics import hamming_loss, \
    accuracy_score, \
    multilabel_confusion_matrix, \
    classification_report


dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_csv_path = str(dir_path.parent.absolute()) + "/data/html_data_preprocessed_class.csv"

pandas_df=pd.read_csv(html_data_csv_path)

pandas_df = pandas_df.fillna("") # some nan in the data, to investigate

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


pandas_df['clean_text_tok']=[nltk.word_tokenize(i) for i in pandas_df['clean_text']]
# model = Word2Vec(pandas_df['clean_text_tok'],min_count=1)
# model.save("Language_models/Word2Vec.model")
path_to_model = str(dir_path.parent.absolute()) + "/Policy-code/Language_models/Word2Vec.model"

model = Word2Vec.load(path_to_model)
w2v = dict(zip(model.wv.index2word, model.wv.vectors))
modelw = MeanEmbeddingVectorizer(w2v)
print(pandas_df[pandas_df.columns[14:-1]])
X_train, X_test, y_train, y_test = train_test_split(pandas_df["clean_text"],pandas_df[pandas_df.columns[14:-1]],test_size=0.3,shuffle=True)

# Word2Vec runs on tokenized sentences
X_train_tok=[nltk.word_tokenize(i) for i in X_train]
X_test_tok=[nltk.word_tokenize(i) for i in X_test]

# converting text to numerical data using Word2Vec
X_train_vectors_w2v = modelw.transform(X_train_tok)
X_test_vectors_w2v = modelw.transform(X_test_tok)

# print(y_train.to_numpy())
# using Multi-label kNN classifier
classifier = MLkNN()
classifier.fit(X=X_train_vectors_w2v, y=y_train.to_numpy())

# dump(mlknn_classifier, 'policy_code_classification/policy_code_classification_model.joblib')
with open('policy_code_classification/policy_code_classification_model.pkl', 'wb') as f:
    pickle.dump(classifier, f)
with open('policy_code_classification/policy_code_classification_model.pkl', 'rb') as f:
    policy_code_classification_model = pickle.load(f)

# policy_code_classification_model = load('policy_code_classification/policy_code_classification_model.joblib')

predicted = policy_code_classification_model.predict(X_test_vectors_w2v)

categories = list(pandas_df.columns.values)

print(accuracy_score(y_test.to_numpy(), predicted))
print(hamming_loss(y_test.to_numpy(), predicted))
print(multilabel_confusion_matrix(y_test.to_numpy(), predicted))
print(classification_report(y_true=y_test.to_numpy(), y_pred=predicted, target_names=categories[14:-1]))