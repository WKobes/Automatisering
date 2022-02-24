import os
from github import Github


def issue_format(issue):
    date = issue.created_at.strftime('%d %b. %Y')
    return f'* {issue.repository.name} [issue #{issue.number}] [{issue.title}]({issue.html_url}) ({date})\n'


g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
labels = org.get_repo('Automatisering').get_labels()
klein = org.get_repo('Automatisering').get_label('Scope: Klein')
groot = org.get_repo('Automatisering').get_label('Scope: Groot')

for label in labels:
    if not label.name.startswith('Overleg: '):
        continue
    name = label.name[label.name.find(': ')+2:]
    content = f'# {name}'
    print(name)
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
