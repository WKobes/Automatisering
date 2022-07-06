import os
from github import Github
import requests


def intro_format(name):
    print('Looking for intro in ' + name)
    path = name
    intro = ''
    agenda = ''
    try:
        contents = repo.get_contents(path=path)
        for entry in contents:
            if entry.name[0] == '2' and entry.type == 'dir':
                path = entry.path
        contents = repo.get_contents(path=path)
        for entry in contents:
            if entry.name.upper() == 'INTRO.MD':
                intro = '\n\n' + requests.get(entry.download_url).text
            elif entry.name.upper() == 'TIJDPLAN.MD':
                agenda = '\n\n' + requests.get(entry.download_url).text
    finally:
        return [path, agenda, intro]


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
    if name == 'TO-DK':
        results = intro_format('Digikoppeling')
    elif name == 'TO-OAuth':
        results = intro_format('OAuth')
    else:
        results = intro_format('Programmeringstafels/' + name)
    fn = f'{results[0]}/README.md'
    content += results[1]  # Agenda
    issues = org.get_issues(filter='all', labels=[label])
    issuesGroot = []
    issuesKlein = []
    issuesOverig = []
    for issue in issues:
        issuesOverig.append(issue)
        for issueLabel in issue.labels:
            if issueLabel.name == groot.name:
                issuesOverig.pop(-1)
                issuesGroot.append(issue)
                break
            elif issueLabel.name == klein.name:
                issuesOverig.pop(-1)
                issuesKlein.append(issue)
                break
    if len(issuesGroot) + len(issuesKlein) + len(issuesOverig) > 0:
        content += '\n# Punten\n'
        if len(issuesGroot) > 0:
            content += '\n## Grote wijzigingen\n'
            for issue in issuesGroot:
                content += issue_format(issue)
        if len(issuesKlein) > 0:
            content += '\n## Kleine wijzigingen\n'
            for issue in issuesKlein:
                content += issue_format(issue)
        if len(issuesOverig) > 0:
            content += '\n## Overige punten\n'
            for issue in issuesOverig:
                content += issue_format(issue)
    intro = results[2]
    if len(intro) > 0:  # Intro.md
        content += '\n# Toelichting\n'
        content += intro
    fn = fn.replace(' ', '-')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    f = open(fn, 'w')
    print('Writing to ' + fn)
    f.write(content)
    f.close()
