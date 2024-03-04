import json
import re
import requests

errors = 0
content = ''

with open('muffet.json') as file:
    data = json.load(file)
    data = sorted(data, key=lambda k: k['url'])
    for page in data:
        if re.search("publicatie\/[^\/]+\/[^\/]+\/$", page['url']):
            content += '\n### ' + page['url'] + '\n'
            page['links'] = sorted(page['links'], key=lambda k: k['url'])
            for link in page['links']:
                errors += 1
                content += '* ' + link['url'] + ' `' + link['error'] + '`' + '\n'

f = open('links.md', 'w')
f.write('## ' + str(errors) + ' broken links\n')
f.write(content)
f.close()
