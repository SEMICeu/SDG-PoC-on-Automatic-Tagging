import json

from ..web.models import Status, EnhanceRequest, EnhanceResponse, MetaTag


def get_status():
    status = Status(True)
    return status

def enhance(request):


    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        metatag = MetaTag(name=i,value="Test1")
        metatags_in_response.append(metatag)

    response = EnhanceResponse(metatags=metatags_in_response)
    return response

