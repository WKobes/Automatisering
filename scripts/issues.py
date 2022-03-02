import os
from github import Github
import requests


# TODO: Clean-up
def intro_format(repo_name):
    print('Looking for intro in ' + repo_name)
    repo = org.get_repo(repo_name)
    contents = repo.get_contents(path='')
    path = ''
    intro = ''
    for entry in contents:
        if entry.name[0] == '2' and entry.type == 'dir':  # Year
            path = entry.path
    if len(path) > 0:
        contents = repo.get_contents(path=path)
        path = ''
        for entry in contents:
            if entry.name[0] == '2' and entry.type == 'dir':  # Date
                path = entry.path
        if len(path) > 0:
            contents = repo.get_contents(path=path)
            for entry in contents:
                if entry.name == 'INTRO.MD':  # Intro
                    intro = '\n\n' + requests.get(entry.download_url).text
                    print(intro)
    return [repo, path, intro]


def issue_format(issue):
    date = issue.created_at.strftime('%d %b. %Y')
    status = ''
    for label in issue.labels:
        if label.name.startswith('Status: '):
            status = f', _{label.name}_'
    return f'* {issue.repository.name} [issue #{issue.number}] [{issue.title}]({issue.html_url}) ({date}){status}\n'


g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
labels = org.get_repo('Automatisering').get_labels()
klein = org.get_repo('Automatisering').get_label('Scope: Klein')
groot = org.get_repo('Automatisering').get_label('Scope: Groot')

for label in labels:
    if not label.name.startswith('Overleg: '):
        continue
    name = label.name[label.name.find(': ') + 2:]
    print(name)
    content = f'# {name}'
    results = []
    if name == 'Technisch overleg':
        results = intro_format('Digikoppeling-Technisch-Overleg')
        content += results[2]
    issues = org.get_issues(filter='all', labels=[label, groot])
    content += '\n## Grote wijzigingen\n'
    for issue in issues:
        content += issue_format(issue)
    issues = org.get_issues(filter='all', labels=[label, klein])
    content += '\n## Kleine wijzigingen\n'
    for issue in issues:
        content += issue_format(issue)
    fn = name.replace(' ', '-')
    f = open(f'issues/{fn}.md', 'w')
    f.write(content)
    f.close()

    if len(results) > 0:
        repo = results[0]
        path = results[1] + '/README.MD'
        text = content
        message = 'Updating notes'
        print(f'Editing {path} in {repo.name}')
        try:
            file = repo.get_contents(path=path)
            sha = file.sha
        except:
            repo.create_file(path=path, message=message, content=text)
        else:
            if requests.get(file.download_url).text == text:
                print('No update')
            else:
                repo.update_file(path=path, message=message, content=text, sha=sha)
