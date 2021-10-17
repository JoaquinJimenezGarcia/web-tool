from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json
import yaml
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/sites_config'
os.chdir(path)

def createJsonString(data):
    data_string = """{
       "account": ["""
    
    for site in data:
        data_string = data_string + """{
             "site": """ + site[0] + """,
             "version": """ + site[1] + """,
             "notBefore": """ + site[2] + """,
             "notAfter": """ + site[3] + """,
          },"""


    data_string = data_string +   """]
    }
    """

    #return json.loads(data_string)
    return data_string

for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".yaml"):
        file_path = f"{path}/{file}"

        with open(file_path, "r") as f:
            config = yaml.load(f)

        sites = config["sites"]
        sites_result = []

        for site in sites:
            print("Checking " + site)
            base_url = site
            port = '443'

            hostname = base_url
            context = ssl.create_default_context()

            site_result = []

            try:
                with socket.create_connection((hostname, port)) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        version = ssock.version()
                        data = json.dumps(ssock.getpeercert())
                        data = json.loads(data)
                        
                        site_result.append(site)
                        site_result.append(version)
                        site_result.append(data['notBefore'])
                        site_result.append(data['notAfter'])
                        
            except socket.error as err:
                print()
                site_result.append(site)
                site_result.append("0")
                site_result.append("0")
                site_result.append("0")

            sites_result.append(site_result)
        
        site_data = createJsonString(sites_result)

        file = file.replace('.yaml', '')
        with open(file+'.json', 'w', encoding='utf-8') as f:
            json.dump(site_data, f, ensure_ascii=False, indent=4)