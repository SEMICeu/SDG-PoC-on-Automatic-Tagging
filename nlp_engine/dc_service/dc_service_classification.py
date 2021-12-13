from joblib import load
import os

def dc_service_classification(vector):
    """

    :param vector: Array
    :return:

    This function gives the tag from the embedding
    """
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    path_to_information_classification_model = dir_path + "/classification_models/DC_Service_Information_classification_model.joblib"
    information_classification_model = load(path_to_information_classification_model)

    path_to_procedure_classification_model = dir_path + "/classification_models/DC_Service_Procedure_classification_model.joblib"
    procedure_classification_model = load(path_to_procedure_classification_model)

    information_classification_result = information_classification_model.predict(vector)
    procedure_classification_result = procedure_classification_model.predict(vector)

    if (information_classification_result == 1) and (procedure_classification_result == 0):
        tag = "information"
    elif (information_classification_result == 0) and (procedure_classification_result == 1):
        tag = "procedure"
    elif (information_classification_result == 1) and (procedure_classification_result == 1):
        tag = "information;procedure"
    else:
        tag = ""

    return tag