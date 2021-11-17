import os

os.chdir("..")

from api.src.nlp_api.web.models import Status, EnhanceRequest, EnhanceResponse, MetaTag

def nlp_engine(request):

    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        metatag = MetaTag(name=i, value="Test1")
        metatags_in_response.append(metatag)

    response = EnhanceResponse(metatags=metatags_in_response)
    return response