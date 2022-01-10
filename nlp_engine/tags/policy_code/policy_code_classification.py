from joblib import load
import os
import sklearn
import pandas as pd
from skmultilearn.adapt import MLkNN
from pathlib import Path
import pickle
def policy_code_classification(vector):
    """

    :param vector: Array
    :return:

    This function gives the dc_policy code tag from the embedding
    """
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    path_to_policy_code_classification_model = dir_path + "/classification_model/policy_code_classification_model.pkl"
    with open(path_to_policy_code_classification_model, 'rb') as f:
        policy_code_classification_model = pickle.load(f)

    # policy_code_classification_model = load(path_to_policy_code_classification_model)

    information_classification_result = policy_code_classification_model.predict(vector).toarray()

    information_classification_result = [i.item() for i in information_classification_result[0]]

    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    path_to_policy_code_taxonomy = str(dir_path.parent.parent.absolute()).replace("\\","/") + "/doc/policy_codes_last_layer.csv"

    policy_code_last_layer = pd.read_csv(filepath_or_buffer=path_to_policy_code_taxonomy,  header=0, sep=",")

    tag = []

    for i in range(len(information_classification_result)):
        if information_classification_result[i]==1:
            tag.append(policy_code_last_layer.loc[i, "Policy code"])

    return ";".join(tag)