import os

os.chdir("..")

from nlp_engine.tags.dc_location.dc_location_tag import dc_location_tag

text="https://www.do.se/other-languages/english/act-concerning-the-equality-ombudsman/"
tag = dc_location_tag(text)

print(tag)
