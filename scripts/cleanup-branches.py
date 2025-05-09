import os
from github import Github

g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
preview_repository = org.get_repo('Publicatie-Preview')

def is_preview_branch(path):
    try:
        preview_repository.get_contents(f"{path}/index.html")
        return True
    except:
        return False

def get_repository_branches(repository_name):
    try:
        specific_repository = org.get_repo(repository_name)
        return [branch.name for branch in specific_repository.get_branches()]
    except:
        print(f"Repository {repository_name} bestaat niet meer en kan geheel worden gedelete")
        return []

all_directories = preview_repository.get_contents("")
for directory in all_directories:
    if directory.type == "file":
        continue
    
    repository_name = directory.path

    print(f"Checken van preview branches voor {repository_name}")

    # Filter nested directories
    # TODO: Verzin een manier om alsnog recursief te kunnen deleten
    preview_branches = [preview_branch.name for preview_branch in preview_repository.get_contents(repository_name) if is_preview_branch(preview_branch.path)]

    repository_branches = get_repository_branches(repository_name)

    for preview_branch in preview_branches:
        if preview_branch not in repository_branches:
            print(f"Kunnen we deleten: {repository_name}/{preview_branch}")
