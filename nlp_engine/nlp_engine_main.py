import os

os.chdir("..")

from api.src.nlp_api.web.models import MetaTag
from nlp_engine.dc_service.dc_service_tag import dc_service_tag
def execute(request):
    print(request)
    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        if i == "sdg-tag":
            tag_value = "Test1"
        elif i == "DC.ISO3166":
            tag_value = "Test1"
        elif i =="DC.location":
            tag_value = "Test1"
        elif i == "DC.service":
            tag_value = dc_service_tag(request.page.elementToExtract)
        elif i == "policy-code":
            tag_value = "Test1"
        elif i == "DC.Policy":
            tag_value = "Test1"
        else:
            tag_value = "This tag does not exist"
        # https://github.com/zalando/connexion/issues/458
        metatag = MetaTag(name=i, value=tag_value).to_dict()
        metatags_in_response.append(metatag)
        print(metatags_in_response)

    return metatags_in_response