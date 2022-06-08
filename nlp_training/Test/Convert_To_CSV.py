import csv
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_json_path = dir_path + "/data/html_data.json"

with open(html_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list = jsonObject['html_list']
# print(html_list)
keys = html_list[0].keys()
# print(keys)
with open('data/html_data.csv', 'w', encoding="utf-8",newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(html_list)