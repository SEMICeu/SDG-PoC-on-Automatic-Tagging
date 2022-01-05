import os

os.chdir("..")

from nlp_engine.tags.dc_iso3166.dc_iso3166_tag import dc_iso3166_tag
from api.src.nlp_api.web.models import MetaTag
from nlp_engine.tags.dc_policy.dc_policy_tag import dc_policy_tag
from nlp_engine.tags.dc_service.dc_service_tag import dc_service_tag
from nlp_engine.tags.policy_code.policy_code_tag import policy_code_tag
from nlp_engine.tags.dc_location.dc_location_tag import dc_location_tag
def execute(request):
    """

    :param request:
    :return: Metatag

    This function takes a request of Metatags (containing the Metatags, the text of the webpage and the URL).
    For each meta tag, this function calls another function that produce the tag.
    While producing the meta tags, this function also set the status of the NLP Engine as busy.
    """
    print(request)

    # set_status_busy()
    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        if i == "sdg-tag":
            tag_value = "sdg"
        elif i == "DC.ISO3166":
            tag_value = dc_iso3166_tag(request.url)
        elif i =="DC.Location":
            tag_value = dc_location_tag(request.url)
        elif i == "DC.Service":
            tag_value = dc_service_tag(request.text)
        elif i == "policy-code":
            tag_value = policy_code_tag(request.text)
        elif i == "DC.Policy":
            tag_value = dc_policy_tag(request.text)
        else:
            tag_value = "This tag does not exist"
        # https://github.com/zalando/connexion/issues/458
        metatag = MetaTag(name=i, value=tag_value).to_dict()
        metatags_in_response.append(metatag)
        print(metatags_in_response)

    # set_status_available()

    return metatags_in_response