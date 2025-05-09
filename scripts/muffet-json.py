import json
import os
import re
import requests
import sys

JSON_PATH = 'muffet.json'

if not os.path.exists(JSON_PATH) or os.path.getsize(JSON_PATH) == 0:
    sys.exit(0)

errors = 0
content = ''

with open(JSON_PATH, 'r',  encoding='utf-8') as input_file:
    # De output van het Node scriptje heeft ook een print regel, dus pak alleen de json
    json_string = input_file.readlines()[1]
    data = json.loads(json_string)
    data = sorted(data, key=lambda k: k['url'])
    for page in data:
        if re.search("publicatie\/", page['url']):
            content += '\n### ' + page['url'] + '\n'
            page['links'] = sorted(page['links'], key=lambda k: k['url'])
            for link in page['links']:
                errors += 1
                content += '* ' + link['url'] + ' `' + link['error'] + '`' + '\n'

if errors == 0:
    print("No errors to report")
    sys.exit(0)

with open('links.md', 'w') as output_file:
    output_file.write('## ' + str(errors) + ' broken links\n')
    output_file.write(content)
