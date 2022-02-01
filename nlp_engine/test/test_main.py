import os

os.chdir("..")

from nlp_engine.tags.dc_location.dc_location_tag import dc_iso3166_tag

text="https://europa.eu/youreurope/citizens/consumers/consumers-dispute-resolution/index_en.htm"
tag = dc_iso3166_tag(text)

print(tag)
