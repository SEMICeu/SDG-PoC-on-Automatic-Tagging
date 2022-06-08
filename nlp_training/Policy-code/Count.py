import pandas as pd
import os
from pathlib import Path
import json

dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_csv_path = str(dir_path.parent.absolute()) + "/data/html_data_translated.csv"

pandas_df = pd.read_csv(html_data_csv_path)
print(len(pandas_df.index))


dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_tagged_json_path = str(dir_path.parent.absolute()) + "/data/html_data_multilingual_Azure.json"

with open(file=html_data_tagged_json_path, encoding="utf-8") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['html_list']

pandas_df = pd.DataFrame(data)

print(len(pandas_df.index))