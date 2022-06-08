import json
import os
from bs4 import BeautifulSoup

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_json_path = dir_path + "/data/html_data_tagged_tagged.json"
print(html_json_path)
with open(html_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list = jsonObject['html_list']
html_list_json_file_tagged = {}
html_list_json_file_tagged['html_list'] = []

for html in html_list:

    soup = BeautifulSoup(html["html"], 'html.parser')

    sdg_tag_header = soup.find(attrs={"name": "sdg-tag"})
    ISO3166_header = soup.find(attrs={"name": "DC.ISO3166"})
    Location_header = soup.find(attrs={"name": "DC.Location"})
    Service_header = soup.find(attrs={"name": "DC.Service"})
    policy_code_header = soup.find(attrs={"name": "policy-code"})
    Policy_header = soup.find(attrs={"name": "DC.Policy"})

    sdg_tag_header.decompose()
    ISO3166_header.decompose()
    Location_header.decompose()
    Service_header.decompose()
    policy_code_header.decompose()
    Policy_header.decompose()

