
import tldextract

def iso3166_tag(url):
    """

    :param body: str
    :return: str

    This function returns the country of url
    """

    extract = tldextract.extract(url)

    domain = extract.suffix

    country = domain.split(".")[-1]

    country_uppercase = country.upper()

    return country_uppercase