import os

os.chdir("..")

from api.src.nlp_api.web.models import MetaTag

def execute(request):
    print(request)
    metatags_in_request = request.metatags
    metatags_in_response = []
    for i in metatags_in_request:
        # https://github.com/zalando/connexion/issues/458
        metatag = MetaTag(name=i, value="Test1").to_dict()
        metatags_in_response.append(metatag)
        print(metatags_in_response)

    return metatags_in_response