import os
from github import Github


def issue_quote(issue):
    quote = f'\n### {issue.title}\n{issue.body}\n'
    quote = quote.replace('\n', '\n>')
    return f'{quote}\n{issue.url}\n'


g = Github(os.environ['SANDERKE'])
org = g.get_organization('Logius-standaarden')
labels = org.get_repo('Automatisering').get_labels()
klein = org.get_repo('Automatisering').get_label('klein')
groot = org.get_repo('Automatisering').get_label('groot')

for label in labels:
    if label.name[0].islower():
        continue
    content = f'# {label.name}'
    print(label.name)
    if (label.name != 'klein') & (label.name != 'groot'):
        issues = org.get_issues(filter='all', labels=[label, groot])
        content += '\n## Grote wijzigingen\n'
        for issue in issues:
            content += issue_quote(issue)
        issues = org.get_issues(filter='all', labels=[label, klein])
        content += '\n## Kleine wijzigingen\n'
        for issue in issues:
            content += issue_quote(issue)
    f = open(f'issues/{label.name}.md', 'w')
    f.write(content)
    f.close()
