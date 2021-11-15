
# define the converter function
def converter():

    import pandas as pd
    import ssl
    import os

    # read excel files with all the urls
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    html_list_excel_file = dir_path + '/cpsv-pilot.xlsx'

    html_list_pandas_file = pd.read_excel(html_list_excel_file)

    # set up the scrapping agent
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    X_Mashape_Key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    headers = {'User-Agent': user_agent,
               'X-Mashape-Key': X_Mashape_Key}
    gcontext = ssl.SSLContext()

    # filter on English HTML pages
    html_list_pandas_file_english = html_list_pandas_file[(html_list_pandas_file.LANGUAGE == 'en')]

    # print(html_list_pandas_file_english)

    from urllib.request import Request, urlopen
    import urllib3
    import json
    from bs4 import BeautifulSoup

    # scrap each english url of the excel file
    html_list_json_file = {}
    html_list_json_file['html_list'] = []
    for index, row in html_list_pandas_file_english.iterrows():
        title = row['TITLE']
        url = row['URL']
        language = row['LANGUAGE']
        classification_information = row['CLASSIFICATION_INFORMATION']
        metadata_type_string = row['METADATA_TYPE_STRING']
        country = row['COUNTRY']
        print(url)
        try:
            request = Request(url=url, headers=headers)
            response = urlopen(request, context=gcontext)
            webContent = response.read()
            soup = BeautifulSoup(webContent, 'html.parser')
            html = soup.prettify()

            # filter the pages according to the tags present in the pages
            if "sdg-tag" in html or "DC.ISO3166" in html or "DC.Location" in html or "DC.Service" in html or "policy-code" in html or "DC.Policy" in html:

                # extract the tags present in the pages (this part can be improved since we don't gather all tags, some of them are not in the format '< meta name: "DC.Example" content: "Example">')
                sdg_tag_header = soup.find(attrs={"name": "sdg-tag"})
                ISO3166_header = soup.find(attrs={"name": "DC.ISO3166"})
                Location_header = soup.find(attrs={"name": "DC.Location"})
                Service_header = soup.find(attrs={"name": "DC.Service"})
                policy_code_header = soup.find(attrs={"name": "policy-code"})
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

                html_list_json_file['html_list'].append({
                    'title': title,
                    'url': url,
                    'language': language,
                    'classification_information': classification_information,
                    'metadata_type_string': metadata_type_string,
                    'country': country,
                    'html': str(html),
                    'sdg_tag': sdg_tag,
                    'ISO3166': ISO3166,
                    'Location': Location,
                    'Service': Service,
                    'policy_code': policy_code,
                    'Policy': Policy
                })
        except:
            print(ValueError)


    with open('data/html_data.json', 'w') as outfile:
        json.dump(html_list_json_file, outfile)

# run the converter function
converter()