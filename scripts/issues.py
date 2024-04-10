import os
from github import Github
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time

def find_path(name):
    path = name.replace(" ", "-")
    print('Looking for path in ' + path)
    try:
        contents = repo.get_contents(path=path)
        for entry in contents:
            if entry.name[0] == '2' and entry.type == 'dir':
                path = entry.path
        contents = repo.get_contents(path=path)
    finally:
        print('Path: ' + path)
        return path


def issue_format(issue):
    date = issue.created_at
    date = format_date(date, format='long', locale='nl_NL')
    status = ''
    pr = ''
    for label in issue.labels:
        if label.name.startswith('Status: '):
            status = f', _{label.name}_'
    events = issue.get_events()
    for event in events:
        if event.event == 'connected' and issue.pull_request is None:
            # href finder from https://stackoverflow.com/a/60780499
            r = requests.get(issue.html_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            issueForm = soup.find("form", {"aria-label": re.compile('Link issues')})
            href = [i["href"] for i in issueForm.find_all("a")]
            r = re.compile('pull\/([^\/]+)\/?$')
            found = list(filter(r.search, href))[0]
            # pullnumber = r.search(found).group(1)            
            pr = f'\n  * [Wijzigingsvoorstel](https://github.com/{found}/files)'
            break
    return f'* {issue.repository.name} [issue #{issue.number}] [{issue.title}]({issue.html_url}) ({date}){status}{pr}\n'


g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
base = org.get_repo('Automatisering')
labels = base.get_labels()
klein = base.get_label('Scope: Klein')
groot = base.get_label('Scope: Groot')
repo = org.get_repo('Overleg')
pt = ["Gegevensuitwisseling", "Infrastructuur", "Interactie", "Toegang"]

split = '<!-- comment niet verwijderen s.v.p. -->'

for label in labels:
    if not label.name.startswith('Overleg: '):
        continue
    name = label.name[label.name.find(': ') + 2:]
    print(f'~ {name} ~')
    titel = name
    path = ''
    if name == 'TO-DK':
        path = find_path('Digikoppeling')
        titel = 'Technisch Overleg Digikoppeling'
    elif name == 'TO-OAuth':
        path = find_path('OAuth')
        titel = 'Technisch Overleg OAuth'
    elif name in pt:
        path = find_path('Programmeringstafels/' + name)
    else:
        path = find_path(name)    
    fn = f'{path}/README.md'
    date = path.split("/")[-1]
    try:
        datetime = datetime.strptime(date, '%Y-%m-%d')
        date = '\n\n' + format_date(datetime, format='full', locale='nl_NL')
        if datetime.date() < datetime.now().date():
            print('Skipping date in past')
            continue
    except:
        print('No date found')
        date = ''
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
        content = f'\n{split}\n<!-- Alles onder deze regel wordt automatisch overschreven -->\n## Onderwerpen\n'
        if len(issuesGroot) > 0:
            content += '\n### Grote wijzigingen\n'
            for issue in issuesGroot:
                content += issue_format(issue)
        if len(issuesKlein) > 0:
            content += '\n### Kleine wijzigingen\n'
            for issue in issuesKlein:
                content += issue_format(issue)
        if len(issuesOverig) > 0:
            content += '\n### Overige punten\n'
            for issue in issuesOverig:
                content += issue_format(issue)
    fn = fn.replace(' ', '-')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    contentPrevious = ''
    try:
        f = open(fn, 'r+')
        contentPrevious = f.read()
    except:
        f = open(fn, 'a+')
        print('No previous content')

    contentList = contentPrevious.split(split)
    if len(contentList) < 3:
        contentList = ['','\n\n<!-- Toelichting, agenda, e.d. kan hier -->\n\n\n','']
    contentList[0] = f'# {titel}{date}\n<!-- Titel en datum zijn automatisch -->\n{split}'
    contentList[2] = content
    content = ''.join(contentList)
    print('Writing to ' + fn)
    f.write(content)
    f.close()
