import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
# for plotting
import seaborn as sns

# for model-building
# bag of words
# for word embedding

############## load the text data ###################
dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_csv_path = str(dir_path.parent.absolute()) + "/data/html_data_translated_preprocessed.csv"

pandas_df = pd.read_csv(html_data_csv_path)

# pandas_df = pandas_df.dropna() # some nan in the data

print(pandas_df.info())

print(pandas_df)

pandas_df_categorization = pd.DataFrame(pandas_df["clean_text"])

############## load the classes ###################

policy_code_classes_csv_path = str(
    dir_path.parent.absolute()) + "/Policy-code/policy_code_classification/policy_codes.csv"

pandas_policy_code_df = pd.read_csv(filepath_or_buffer=policy_code_classes_csv_path, header=0, sep=";")

length = []

for index, row in pandas_policy_code_df.iterrows():
    length.append(len(row["Policy code"]))

pandas_policy_code_df["Length"] = length

pandas_policy_code_df = pandas_policy_code_df[pandas_policy_code_df["Length"] == 2]

pandas_policy_code_df.to_csv(path_or_buf=str(dir_path.parent.absolute()) + "/data/policy_codes_last_layer.csv", index=False)

############## Add the columns of the classes to the data ###################

for index_policy_code, row_policy_code in pandas_policy_code_df.iterrows():
    code = []
    # print("############ Policy code tag ############")
    # print(row_policy_code["Policy code"])
    for index_data, row_data in pandas_df.iterrows():
        classification_information_tag = row_data["classification_information"].split(";")
        # print("classification_information:")
        # print(row_data["classification_information"])
        # print(classification_information_tag)
        policy_code_tag=0
        for i in classification_information_tag:
            # print("i:")
            # print(i)
            if row_policy_code["Policy code"] == i:
                # print("add tag")
                policy_code_tag=1
        code.append(policy_code_tag)
    code_string = row_policy_code["Policy code"]
    # print(code)
    pandas_df[code_string] = code

print(pandas_df.info())

print(pandas_df)

############## Plot the repartition of the data on the categories  ###################

# categories = list(pandas_df.columns.values)
# print(categories)
# sns.set(font_scale=0.5)
# plt.figure(figsize=(15, 8))
# ax = sns.barplot(x=categories[14:], y=pandas_df.iloc[:, 14:].sum().values)
# plt.title("Amount of data for each Policy code", fontsize=24)
# plt.ylabel('Number of data', fontsize=18)
# plt.xlabel('Policy code', fontsize=18)
# # adding the text labels
# rects = ax.patches
# labels = pandas_df.iloc[:, 14:].sum().values
# for rect, label in zip(rects, labels):
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2,
#             height + 5,
#             label,
#             ha='center',
#             va='bottom',
#             fontsize=6)
# plt.show()

############## Create the data with the cleaned columns  ###################


pandas_df.to_csv(path_or_buf=str(dir_path.parent.absolute()) + "/data/html_data_translated_preprocessed_class.csv", index=False)
