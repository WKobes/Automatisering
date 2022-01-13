import json

errors = 0
content = ''

with open('muffet.json') as file:
    data = json.load(file)
    for page in data:
        content += '### ' + page['url'] + '\n'
        for link in page['links']:
            errors += 1
            content += '* ' + link['url'] + ' `' + link['error'] + '`' + '\n\n'

f = open('links.md', 'w')
f.write('## ' + str(errors) + ' broken links\n\n')
f.write(content)   
f.close()
