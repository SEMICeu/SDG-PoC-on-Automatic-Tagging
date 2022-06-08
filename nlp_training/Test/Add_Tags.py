import json
import os

from bs4 import BeautifulSoup

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_data_tagged_json_path = dir_path + "/data/html_data_tagged.json"
print(html_data_tagged_json_path)
with open(html_data_tagged_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

html_list_json_file_tagged = jsonObject['html_list']
html_list_json_file_tagged_add_tag = {}
html_list_json_file_tagged_add_tag['html_list'] = []

for html in html_list_json_file_tagged:
    soup = BeautifulSoup(html["html"], 'html.parser')

    print("*******************")
    print(html['url'])

    sdg_tag_header = soup.find(attrs={"name": "sdg-tag"})
    ISO3166_header = soup.find(attrs={"name": "DC.ISO3166"})
    Location_header = soup.find(attrs={"name": "DC.Location"})
    Service_header = soup.find(attrs={"name": "DC.Service"})
    policy_code_header = soup.find(attrs={"name": "policy-code"})
    Policy_header = soup.find(attrs={"name": "DC.Policy"})


    # print(sdg_tag_header)
    # print(ISO3166_header)
    # print(Location_header)
    # print(Service_header)
    # print(policy_code_header)
    # print(Policy_header)

    if sdg_tag_header is not None:
        sdg_tag = sdg_tag_header["content"]
    else:
        sdg_tag = ""

    if ISO3166_header is not None:
        ISO3166 = ISO3166_header["content"]
    else:
        ISO3166 = ""

    if Location_header is not None:
        Location = Location_header["content"]
    else:
        Location = ""

    if Service_header is not None:
        Service = Service_header["content"]
    else:
        Service = ""

    if policy_code_header is not None:
        policy_code = policy_code_header["content"]
    else:
        policy_code = ""

    if Policy_header is not None:
        Policy = Policy_header["content"]
    else:
        Policy = ""

    print(sdg_tag)
    print(ISO3166)
    print(Location)
    print(Service)
    print(policy_code)
    print(Policy)

    html['sdg_tag'] = sdg_tag
    html['ISO3166'] = ISO3166
    html['Location'] = Location
    html['Service'] = Service
    html['policy_code'] = policy_code
    html['Policy'] = Policy

    html_list_json_file_tagged_add_tag['html_list'].append({
        'title': html["title"],
        'url': html["url"],
        'language': html["language"],
        'classification_information': html["classification_information"],
        'metadata_type_string': html["metadata_type_string"],
        'country': html["country"],
        'html': html["html"],
        'sdg_tag': sdg_tag,
        'ISO3166': ISO3166,
        'Location': Location,
        'Service': Service,
        'policy_code': policy_code,
        'Policy': Policy
    })


with open('../data/html_data_tagged_tagged.json', 'w') as outfile:
    json.dump(html_list_json_file_tagged_add_tag, outfile)