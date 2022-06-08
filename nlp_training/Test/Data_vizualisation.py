import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_json_path = dir_path + "/data/html_data.json"
print(html_json_path)
with open(html_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list = jsonObject['html_list']
html_list_json_file_tagged = {}
html_list_json_file_tagged['html_list'] = []
n = 0
for i in html_list:
    result = "sdg-tag" in i["html"] or "DC.ISO3166" in i["html"] or "DC.Location" in i["html"] or "DC.Service" in i["html"] or "policy-code" in i["html"] or "DC.Policy" in i["html"]

    if result:
        html_list_json_file_tagged['html_list'].append({
            'title': i["title"],
            'url': i["url"],
            'language': i["language"],
            'classification_information': i["classification_information"],
            'metadata_type_string': i["metadata_type_string"],
            'country': i["country"],
            'html': i["html"]
        })
        n = n +1

with open('../data/html_data_tagged.json', 'w') as outfile:
    json.dump(html_list_json_file_tagged, outfile)

print(n)