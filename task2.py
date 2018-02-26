#!/usr/bin/python

import json
import requests
import sys
import os
from urllib.parse import quote


url = "http://api.meaningcloud.com/lang-2.0"

keyvalue = "0d67b1a032357fccd83a37bc90db94bf"


if len(sys.argv) < 2:
    print("No file specified.")
    sys.exit()

filename = sys.argv[1]
if not os.path.isfile(filename):
    print("File dosen't exist.")
    sys.exit()
    
if os.stat(filename).st_size == 0:
    print("File is empty.")
    sys.exit()
    
f = open(filename)
text = f.read()
f.closed

text = quote(text)
payload = "key=" + keyvalue + "&txt=" + text
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)

data = json.loads(response.text)

for language in data['language_list']:
    print(language['name'])
