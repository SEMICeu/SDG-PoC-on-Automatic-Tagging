import os

os.chdir("..")
print(os.getcwd())
from api.src.nlp_api.web.models import Status, EnhanceRequest, EnhanceResponse, MetaTag

def nlp_engine():
    return