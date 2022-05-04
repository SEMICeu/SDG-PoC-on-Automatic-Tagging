import json
import time
import uuid
from pathlib import Path

import requests
import yaml
from langdetect import detect


def get_config():
    my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
    config_path = my_path.parent / 'config.yaml'
    with config_path.open() as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def detectlanguage(text):
    start_time = time.time()

    language = detect(text)
    # your code
    elapsed_time = time.time() - start_time
    print("detect time: " + elapsed_time)
    print("detected language: " + language)
    return language

def translate(texttotranslate, languagefrom, languageto):

    # Add your key and endpoint
    config = get_config()
    key = config['translate']['key']
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "francecentral"

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
    return response["translations"][0]["text"]
