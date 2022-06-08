

# use text classification to have the DC.Service tag
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_json_path = dir_path + "/data/html_data_tagged_tagged.json"

with open(html_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list = jsonObject['html_list']

html_text, information_class, procedure_class = [], [], []
for html in html_list:
    html_text =
information_data =