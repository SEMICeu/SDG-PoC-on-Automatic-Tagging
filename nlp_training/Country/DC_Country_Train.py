import json
import socket
from geolite2 import geolite2

def origin(ip, domain_str, result):
    print("{0} [{1}]: {2}".format(domain_str.strip(), ip, result))

def getip(domain_str):
    ip = socket.gethostbyname(domain_str.strip())
    reader = geolite2.reader()
    output = reader.get(ip)
    result = output['country']['iso_code']
    origin(ip, domain_str, result)

with open(html_data_tagged_json_path) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()


dir_path = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))

html_data_tagged_json_path = str(dir_path.parent.absolute()) + "/data/html_data.json"


data = jsonObject['html_list']

for i in range(len(data)):
    try:
        getip(data[i]["url"])
    except socket.error as msg:
        print("{0} [could not resolve]".format(data[i]["url"].strip()))
        if len(data[i]["url"]) > 2:
            subdomain = data[i]["url"].split('.', 1)[1]
            try:
                getip(subdomain)
            except:
                continue

geolite2.close()

