# from dc_service_preprocessing import dc_service_preprocessing
# from dc_service_embedding import dc_service_embedding
# from dc_service_classification import dc_service_classification
from Get_tags.nlp_engine.tags.dc_service.dc_service_classification import dc_service_classification
from Get_tags.nlp_engine.utils.embedding import embedding
from Get_tags.nlp_engine.utils.preprocessing import preprocessing


def dc_service_tag(body: str):
    """

    :param body: str
    :return: str

    This function returns the tag of DC.Service from the body of a webpage.
    This tag can be  'Procedure', 'Information' or both
    """

    preprocessed_body = preprocessing(body)

    embedded_body = embedding(preprocessed_body)

    tag = dc_service_classification(embedded_body)

    if tag == "":
        tag = "404"

    return tag