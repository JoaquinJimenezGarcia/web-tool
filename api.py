from flask import Flask
import json
import os

app = Flask(__name__)

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

app.run(host='0.0.0.0', port=81)