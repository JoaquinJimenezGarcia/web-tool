from flask import Flask
from flask_cors import CORS
import json
import os
from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError

app = Flask(__name__)
CORS(app)

@app.route('/<user>')
def index(user):
    # Opening JSON file
    f = open(os.path.dirname(os.path.abspath(__file__)) + '/sites_config/' + user + '.json')
    
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Closing file
    f.close()
    return data

@app.route('/site/<site>')
def site(site):
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

    site_result = json.dumps(site_result)  
    
    return site_result

app.run(host='0.0.0.0', port=81)