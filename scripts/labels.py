import os
from github import Github

g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
repos = org.get_repos()
labels = org.get_repo('Automatisering').get_labels()

for repo in repos:
    if repo.name == 'Automatisering':
        continue
    print('* Checking ' + repo.name)
    try:
        repo_labels = repo.get_labels()
        for label in labels:
            found = False
            for repo_label in repo_labels:
                if repo_label.name.upper() == label.name.upper():
                    if (repo_label.name != label.name) or (repo_label.description != label.description):
                        repo_label.edit(name=label.name, color=label.color, description=label.description)
                        print(f'Edited label \'{label.name}\' with description \'{label.description}\'')
                    found = True
                    break
            if not found:
                repo.create_label(name=label.name, color=label.color, description=label.description)
                print(f'Created label \'{label.name}\'')
    except:
        print('Could not update labels in ' + repo.name)
