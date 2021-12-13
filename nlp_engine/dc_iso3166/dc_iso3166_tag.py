
import tldextract

def dc_iso3166_tag(url):
    """

    :param body: str
    :return: str

    This function returns the country of url
    """

    extract = tldextract.extract(url)

    domain = extract.suffix

    country = domain.split(".")[-1]

    country_uppercase = country.upper()

    if country_uppercase == "":
        country_uppercase = "404"

    return country_uppercase