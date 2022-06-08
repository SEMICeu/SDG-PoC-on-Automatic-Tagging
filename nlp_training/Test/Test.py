from urllib.request import Request, urlopen
import urllib3
import json
from bs4 import BeautifulSoup
import ssl

# input = input.replace("!web ", "")

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
X_Mashape_Key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
headers = {'User-Agent': user_agent,
           'X-Mashape-Key': X_Mashape_Key}

gcontext = ssl.SSLContext()  # Only for gangstars

url = 'https://www.pts.se/en/english-b/post/permit-application/'
request = Request(url=url, headers=headers)
response = urlopen(request, context= gcontext)
webContent = response.read()
soup = BeautifulSoup(webContent, 'html.parser')
html_text = soup.get_text()

# print(html_text)

# extract the tags present in the pages (this part can be improved since we don't gather all tags, some of them are not in the format '< meta name: "DC.Example" content: "Example">')
sdg_tag_header = soup.find(attrs={"name": "sdg-tag"})
ISO3166_header = soup.find(attrs={"name": "DC.ISO3166"})
Location_header = soup.find(attrs={"name": "DC.Location"})
Service_header = soup.find(attrs={"name": "DC.Service"})
policy_code_header = soup.find(attrs={"name": "policy-code"})
Policy_header = soup.find(attrs={"name": "DC.Policy"})

# print(sdg_tag_header)
# print(ISO3166_header)
# print(ISO3166_header["content"])
# print(Location_header)
# print(Service_header)
# print(policy_code_header)
# print(Policy_header)

# extract the data from the header and remove it from the URL

if ISO3166_header is not None:
    ISO3166 = ISO3166_header["content"]
    ISO3166_header.decompose()
else:
    ISO3166 = ""

if Location_header is not None:
    Location = Location_header["content"]
    Location_header.decompose()
else:
    Location = ""

if Service_header is not None:
    Service = Service_header["content"]
    Service_header.decompose()
else:
    Service = ""

if policy_code_header is not None:
    policy_code = policy_code_header["content"]
    policy_code_header.decompose()
else:
    policy_code = ""

if Policy_header is not None:
    Policy = Policy_header["content"]
    Policy_header.decompose()
else:
    Policy = ""

if sdg_tag_header is not None:
    sdg_tag = sdg_tag_header["content"]
    sdg_tag_header.decompose()
else:
    sdg_tag = ""

print(sdg_tag)
print(ISO3166)
print(Location)
print(Service)
print(policy_code)
print(Policy)
