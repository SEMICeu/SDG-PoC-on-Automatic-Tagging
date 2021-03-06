import json
import time
import uuid
from pathlib import Path

import requests
import yaml
from langdetect import detect

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path


#for model-building

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score

# bag of words

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


def get_config():
    my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
    config_path = my_path.parent / 'configtranslate.yaml'
    with config_path.open() as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def detectlanguage(text):
    # start_time = time.time()

    language = detect(text)
    # your code
    # elapsed_time = time.time() - start_time
    # print("detect time: " + str(elapsed_time))
    # print("detected language: " + language)
    return language

def translate(texttotranslate, languagefrom, languageto):

    # Add your key and endpoint
    config = get_config()
    key = config['translate']['key']
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "westeurope"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': languagefrom,
        'to': [languageto]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': texttotranslate
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return response[0]['translations'][0]['text']



dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_tagged_json_path = str(dir_path.parent.absolute()) + "/data/html_data_multilingual.json"

with open(file=html_data_tagged_json_path, encoding="utf-8") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['html_list']

pandas_df = pd.DataFrame(data)
print(pandas_df.info())

x=pandas_df['classification_information'].value_counts()
print(x)

pandas_df['html'] = pandas_df['html'].apply(lambda x: translate(x[:500], detectlanguage(x), 'en') if(detectlanguage(x) != 'en') else x)

pandas_df.to_csv(path_or_buf=str(dir_path.parent.absolute()) + "/data/html_data_translated.csv", index=False)