# use text classification to have the DC.Service tag
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_json_path = dir_path + "/data/html_data.json"

with open(html_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list = jsonObject['html_list']

title = {}
url = {}
language = {}
classification_information = {}
metadata_type_string = {}
country = {}
body = {}
sdg_tag = {}
ISO3166 = {}
Location = {}
Service = {}
policy_code = {}
Policy = {}

for i in range(len(html_list)):
    num = str(i)
    title[num]=html_list[i]["title"]
    url[num] = html_list[i]["url"]
    language[num]=html_list[i]["language"]
    classification_information[num]= html_list[i]["classification_information"]
    metadata_type_string[num]= html_list[i]["metadata_type_string"]
    country[num]= html_list[i]["country"]
    body[num]= html_list[i]["html"]
    sdg_tag[num]= html_list[i]["sdg_tag"]
    ISO3166[num]= html_list[i]["ISO3166"]
    Location[num]= html_list[i]["Location"]
    Service[num]= html_list[i]["Service"]
    policy_code[num]= html_list[i]["policy_code"]
    Policy[num]= html_list[i]["Policy"]

json_file = {
    'title': title,
    'url': url,
    'language': language,
    'classification_information': classification_information,
    'metadata_type_string': metadata_type_string,
    'country': country,
    'body': body,
    'sdg_tag': sdg_tag,
    'ISO3166': ISO3166,
    'Location': Location,
    'Service': Service,
    'policy_code': policy_code,
    'Policy': Policy

}
with open('../data/html_data_other_format.json', 'w') as outfile:
    json.dump(json_file, outfile)