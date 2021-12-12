from joblib import load
import os
import pandas as pd

def policy_code_classification(vector):
    """

    :param vector: Array
    :return:

    This function gives the policy code tag from the embedding
    """
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    path_to_policy_code_classification_model = dir_path + "/classification_model/policy_code_classification_model.joblib"
    policy_code_classification_model = load(path_to_policy_code_classification_model)

    information_classification_result = policy_code_classification_model.predict(vector).toarray()

    dir_path = os.path.dirname(os.path.realpath(__file__).parent.parent).replace("\\", "/")

    path_to_policy_code_taxonomy = dir_path + "/doc/policy_code_last_layer.csv"

    policy_code_last_layer = pd.read_csv(path_to_policy_code_taxonomy)

    tag = []

    for i in range(len(information_classification_result)):
        if information_classification_result[i]==1:
            tag.append(policy_code_last_layer.loc[i, "Policy code"])

    return ";".join(tag)