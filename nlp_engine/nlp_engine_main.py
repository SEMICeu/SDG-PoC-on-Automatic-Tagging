import os
import time
os.chdir("..")

from api.src.nlp_api.web.models import MetaTag
from nlp_engine.dc_service.dc_service_tag import dc_service_tag
from nlp_engine.nlp_engine_status.status import set_status_busy, set_status_available
def execute(request):
    """

    :param request:
    :return: Metatag

    This function takes a request of Metatags (containing the Metatags, the text of the webpage and the URL).
    For each meta tag, this function calls another function that produce the tag.
    While producing the meta tags, this function also set the status of the NLP Engine as busy.
    """
    print(request)

    set_status_busy()
    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        if i == "sdg-tag":
            tag_value = "sdg"
        elif i == "DC.ISO3166":
            tag_value = "Tag of DC.ISO3166: still work in progress"
        elif i =="DC.location":
            tag_value = "Tag of DC.location: still work in progress"
        elif i == "DC.service":
            tag_value = dc_service_tag(request.text)
        elif i == "policy-code":
            tag_value = "Tag of policy-code: still work in progress"
        elif i == "DC.Policy":
            tag_value = "Tag of DC.Policy: still work in progress"
        else:
            tag_value = "This tag does not exist"
        # https://github.com/zalando/connexion/issues/458
        metatag = MetaTag(name=i, value=tag_value).to_dict()
        metatags_in_response.append(metatag)
        print(metatags_in_response)

    set_status_available()

    return metatags_in_response