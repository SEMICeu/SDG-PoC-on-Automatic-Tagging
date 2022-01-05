

from nlp_engine.tags.dc_iso3166.dc_iso3166_tag import dc_iso3166_tag
from pathlib import Path
import os
import pandas as pd

def dc_location_tag(url):
    """

    :param body: str
    :return: str

    This function returns the nut version of the country of the url
    """

    country = dc_iso3166_tag(url)

    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    path_to_nuts_taxonomy = str(dir_path.parent.absolute()).replace("\\","/") + "/dc_location/nuts/nuts-1-3.csv"

    nuts_1_3 = pd.read_csv(filepath_or_buffer=path_to_nuts_taxonomy,  header=0, sep=";")

    location = ""
    for index_nuts, row_nuts in nuts_1_3.iterrows():
        if row_nuts["nut3"] == country:
            location = row_nuts["label"]

    if location == "":
        location = "404"

    return location