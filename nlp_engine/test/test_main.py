import os
import time


os.chdir("..")
from nlp_engine.dc_iso3166.dc_iso3166_tag import dc_iso3166_tag
from nlp_engine.policy_code.policy_code_classification import policy_code_classification
from nlp_engine.utils.embedding import embedding
from nlp_engine.utils.preprocessing import preprocessing

from nlp_engine.dc_location.dc_location_tag import dc_location_tag



from nlp_engine.nlp_engine_main import execute
from api.src.nlp_api.web.models import MetaTag

text="https://www.do.se/other-languages/english/act-concerning-the-equality-ombudsman/"
tag = dc_location_tag(text)

print(tag)
