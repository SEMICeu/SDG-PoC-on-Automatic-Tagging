import csv
import os
from pathlib import Path
import json
import pandas as pd

os.chdir("..")

from nlp_engine.tags.dc_iso3166.dc_iso3166_tag import dc_iso3166_tag
from nlp_engine.tags.dc_policy.dc_policy_tag import dc_policy_tag
from nlp_engine.tags.dc_service.dc_service_tag import dc_service_tag
from nlp_engine.tags.policy_code.policy_code_tag import policy_code_tag
from nlp_engine.tags.dc_location.dc_location_tag import dc_location_tag


dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

html_data_tagged_json_path = dir_path + "/data/html_data.json"

with open(html_data_tagged_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['html_list']

pandas_df = pd.DataFrame(data)
print(pandas_df.columns)
sdg_tag_result= []
DC_ISO3166_result= []
DC_Location_result= []
DC_Service_result= []
policy_code_result= []
DC_Policy_result= []

for i in range(len(pandas_df.index)):
    print(i)
    # set_status_busy()
    metatags_in_response = []

    sdg_tag_result.append("sdg")

    DC_ISO3166_result.append(dc_iso3166_tag(pandas_df.loc[i, "url"]))

    DC_Location_result.append(dc_location_tag(pandas_df.loc[i, "url"]))

    DC_Service_result.append(dc_service_tag(pandas_df.loc[i, "html"]))

    policy_code_result.append(policy_code_tag(pandas_df.loc[i, "html"]))

    DC_Policy_result.append(dc_policy_tag(pandas_df.loc[i, "html"]))


pandas_df["sdg_tag"]=sdg_tag_result

pandas_df["ISO3166"]=DC_ISO3166_result

pandas_df["Location"]=DC_Location_result

pandas_df["Service"]=DC_Service_result

pandas_df["policy_code"]=policy_code_result

pandas_df["Policy"]=DC_Policy_result

pandas_df.drop("html", axis=1, inplace=True)

pandas_df.to_csv('final_result.csv', sep=';', encoding='utf-8')
