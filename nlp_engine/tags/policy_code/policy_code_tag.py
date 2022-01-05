from nlp_engine.utils.embedding import embedding
from nlp_engine.utils.preprocessing import preprocessing
from nlp_engine.tags.policy_code import policy_code_classification


def policy_code_tag(body: str):
    """

    :param body: str
    :return: str

    This function returns the tag of dc_policy code from the body of a webpage.
    The different tags can be found in doc/policy_codes.csv
    """

    preprocessed_body = preprocessing(body)

    embedded_body = embedding(preprocessed_body)

    tag = policy_code_classification(embedded_body)

    if tag == "":
        tag = "404"

    return tag