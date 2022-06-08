
import tldextract
from worldlib.database import Database
import pycountry

def dc_iso3166_tag(url):
    """

    :param body: str
    :return: str

    This function returns the country of url
    """

    extract = tldextract.extract(url)

    domain = extract.suffix

    country = domain.split(".")[-1]

    db = Database()

    country_tag = db.lookup_code(country)
    try:
        pycountry_result = pycountry.countries.get(name=country_tag)

        iso3166_tag = pycountry_result.alpha_2

        if iso3166_tag == "":
            iso3166_tag = "404"
    except:
        iso3166_tag = "404"

    return iso3166_tag