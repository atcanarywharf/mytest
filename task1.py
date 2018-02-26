#!/usr/bin/python

import json
import requests
import sys
from urllib.parse import quote


url = "http://api.meaningcloud.com/lang-2.0"

keyvalue = "0d67b1a032357fccd83a37bc90db94bf"
text = input('Please input your text:')

if text.strip() == "":
    print("Text is empty.")
    sys.exit()
    
text = quote(text)
payload = "key=" + keyvalue + "&txt=" + text
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)

data = json.loads(response.text)

for language in data['language_list']:
    print(language['name'])
