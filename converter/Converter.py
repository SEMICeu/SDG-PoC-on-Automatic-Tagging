
# define the converter function
import json
import os
import re
import socket
import ssl
import time
import urllib.request
from datetime import datetime
from http.client import IncompleteRead
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import pandas as pd
import yaml
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_config():
    my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
    config_path = my_path.parent / 'config.yaml'
    with config_path.open() as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config


def search(a_list, value):
    try:
        return a_list.index(value)
    except ValueError:
        return None


def converter():
    start_time = datetime.now()
    # read excel files with all the urls
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    config = get_config()
    html_list_excel_file = dir_path + '/' + config['file']['input']

    html_list_pandas_file = pd.read_excel(html_list_excel_file)

    # set up the scrapping agent
    headers = {'User-Agent': config['request']['header']['user_agent'],
               'X-Mashape-Key': config['request']['header']['x_mashape_key'],
               'Connection': config['request']['header']['connection']}
    gcontext = ssl.SSLContext()

    # filter on English HTML pages
    html_list_pandas_file_english = html_list_pandas_file[(html_list_pandas_file.LANGUAGE == config['filter']['language'])]
    print("rows:" + str(len(html_list_pandas_file_english)))
    # browser = webdriver.Chrome()

    # html_list_pandas_file_english = html_list_pandas_file_english[(html_list_pandas_file.COUNTRY == config['filter']['country'])]
    # print(html_list_pandas_file_english)

    # scrap each english url of the excel file
    html_list_json_file = {}
    html_list_json_file['html_list'] = []
    list_url = config['selenium']['url_list']

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)

    for index, row in html_list_pandas_file_english.iterrows():
        title = row['TITLE']
        url = requote_uri(row['URL'])
        language = row['LANGUAGE']
        classification_information = row['CLASSIFICATION_INFORMATION']
        metadata_type_string = row['METADATA_TYPE_STRING']
        country = row['COUNTRY']
        print("url: " + url)
        parsed_uri = urlparse(url)
        parent_uri = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        # print("Parent url: " + parent_uri)
        try:
            found = search(list_url, parent_uri)
            if found is not None:
                print("found: " + parent_uri)

                browser.get(url)
                # print("selector:" + config['selectors'][found])
                try:
                    WebDriverWait(browser, config['selenium']['timeout']).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, config['selenium']['selectors'][found]))
                    )
                except TimeoutException:
                    print("Timed out waiting for page to load")
                webContent = browser.page_source

            else:
                request = Request(url=url, headers=headers)
                response = urlopen(request, context=gcontext, timeout=config['request']['timeout'])
                webContent = response.read()

            soup = BeautifulSoup(webContent, 'html.parser')
            html = soup.prettify()
            # filter the pages according to the tags present in the pages
            if "sdg-tag" in html or "DC.ISO3166" in html or "DC.Location" in html or "DC.Service" in html or "dc_policy-code" in html or "DC.Policy" in html:

                # extract the tags present in the pages (this part can be improved since we don't gather all tags, some of them are not in the format '< meta name: "DC.Example" content: "Example">')
                sdg_tag_header = soup.find(attrs={"name": "sdg-tag"})
                ISO3166_header = soup.find(attrs={"name": "DC.ISO3166"})
                Location_header = soup.find(attrs={"name": "DC.Location"})
                Service_header = soup.find(attrs={"name": "DC.Service"})
                policy_code_header = soup.find(attrs={"name": "dc_policy-code"})
                Policy_header = soup.find(attrs={"name": "DC.Policy"})

                if sdg_tag_header is not None:
                    sdg_tag = sdg_tag_header["content"]
                else:
                    sdg_tag = ""

                if ISO3166_header is not None:
                    ISO3166 = ISO3166_header["content"]
                else:
                    ISO3166 = ""

                if Location_header is not None:
                    Location = Location_header["content"]
                else:
                    Location = ""

                if Service_header is not None:
                    Service = Service_header["content"]
                else:
                    Service = ""

                if policy_code_header is not None:
                    policy_code = policy_code_header["content"]
                else:
                    policy_code = ""

                if Policy_header is not None:
                    Policy = Policy_header["content"]
                else:
                    Policy = ""

                title = title.replace('\t', '')
                text = soup.get_text()
                text = text.replace('\n', ' ').replace('\t', ' ')
                text = re.sub('\s{2,}', ' ', text)
                html_list_json_file['html_list'].append({
                    'title': title,
                    'url': url,
                    'language': language,
                    'classification_information': classification_information,
                    'metadata_type_string': metadata_type_string,
                    'country': country,
                    'html': text,
                    'sdg_tag': sdg_tag,
                    'ISO3166': ISO3166,
                    'Location': Location,
                    'Service': Service,
                    'policy_code': policy_code,
                    'Policy': Policy
                })
            pause_exception_list = config['pause']['exception']['url_list']
            found = search(pause_exception_list, parent_uri)
            if found is not None:
                print("increasing pause for " + parent_uri)
                time.sleep(config['pause']['exception']['time'])
            else:
                print("pause for " + parent_uri)
                time.sleep(config['pause']['time'])

        except urllib.request.HTTPError as e:
            if e.code == 404:
                print(f"{url} is not found")
                continue
        except urllib.error.URLError as e:
            print(f"{url} has error" + str(e))
            continue
        except socket.timeout as e:
            print(f"{url} has socket timeout" + str(e))
            continue
        except IncompleteRead as e:
            print(f"{url} has incomplete read" + str(e))
            continue
        except ValueError as e:
            print("Value error" + str(e))
            continue

    browser.quit()
    with open(config['file']['output'], 'w') as outfile:
        json.dump(html_list_json_file, outfile)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))


# run the converter function
converter()
