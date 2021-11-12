# Read excel file

import pandas as pd
import ssl
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

html_list_excel_file = dir_path + '/cpsv-pilot.xlsx'

html_list_pandas_file = pd.read_excel(html_list_excel_file)

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
X_Mashape_Key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
headers = {'User-Agent': user_agent,
           'X-Mashape-Key': X_Mashape_Key}
gcontext = ssl.SSLContext()

# filter on English HTML pages
html_list_pandas_file_english = html_list_pandas_file[(html_list_pandas_file.LANGUAGE == 'en')]

from urllib.request import Request, urlopen
import json
from bs4 import BeautifulSoup

html_list_json_file = {}
html_list_json_file['html_list'] = []
for index, row in html_list_pandas_file_english.iterrows():

    url = row['URL']
    print(url)
    try:
        request = Request(url=url, headers=headers)
        response = urlopen(request, context=gcontext)
        webContent = response.read()
        soup = BeautifulSoup(webContent, 'html.parser')
        html_body = soup.body
        html_list_json_file['html_list'].append({
            'url': url,
           'html_body': str(html_body)
        })
    except:
        print(ValueError)


with open('data/html_data.json', 'w') as outfile:
    json.dump(html_list_json_file, outfile)