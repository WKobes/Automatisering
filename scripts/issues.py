import os
from github import Github
import requests


def intro_format(name):
    print('Looking for intro in ' + name)
    path = name
    intro = ''
    try:
        contents = repo.get_contents(path=path)
        for entry in contents:
            if entry.name[0] == '2' and entry.type == 'dir':
                path = entry.path
        contents = repo.get_contents(path=path)
        for entry in contents:
            if entry.name == 'intro.md':
                intro = '\n\n' + requests.get(entry.download_url).text
    finally:
        return [path, intro]


def issue_format(issue):
    date = issue.created_at.strftime('%d %b. %Y')
    status = ''
    for label in issue.labels:
        if label.name.startswith('Status: '):
            status = f', _{label.name}_'
    return f'* {issue.repository.name} [issue #{issue.number}] [{issue.title}]({issue.html_url}) ({date}){status}\n'


g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
base = org.get_repo('Automatisering')
labels = base.get_labels()
klein = base.get_label('Scope: Klein')
groot = base.get_label('Scope: Groot')
repo = org.get_repo('Overleg')

for label in labels:
    if not label.name.startswith('Overleg: '):
        continue
    name = label.name[label.name.find(': ') + 2:]
    print(f'~ {name} ~')
    content = f'# {name}'
    results = []
    if name == 'Technisch overleg':
        results = intro_format('Digikoppeling')
    else:
        results = intro_format('Programmeringstafels/' + name)
    fn = f'{results[0]}/README.md'
    content += results[1]
    issues = org.get_issues(filter='all', labels=[label, groot])
    content += '\n## Grote wijzigingen\n'
    for issue in issues:
        content += issue_format(issue)
    issues = org.get_issues(filter='all', labels=[label, klein])
    content += '\n## Kleine wijzigingen\n'
    for issue in issues:
        content += issue_format(issue)
    fn = fn.replace(' ', '-')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    f = open(fn, 'w')
    print('Writing to ' + fn)
    f.write(content)
    f.close()
