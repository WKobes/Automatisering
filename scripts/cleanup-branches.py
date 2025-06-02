import os
import shutil
from pathlib import Path
from github import Github

g = Github(os.environ['BEHEER'])
org = g.get_organization('Logius-standaarden')
PREVIEW_DIRECTORY = Path(os.getcwd())

def is_preview_branch(directory):
    return os.path.exists(os.path.join(directory, "index.html"))

def get_repository_branches(repository_name):
    try:
        specific_repository = org.get_repo(repository_name)
        return [branch.name for branch in specific_repository.get_branches()]
    except:
        print(f"Repository {repository_name} bestaat niet meer en kan geheel worden gedelete")
        return []

all_directories = [f.name for f in os.scandir(PREVIEW_DIRECTORY) if f.is_dir() ]
for repository_name in all_directories:
    print(f"Checken van preview branches voor {repository_name}")

    # Filter nested directories
    # TODO: Verzin een manier om alsnog recursief te kunnen deleten
    preview_branches = [preview_branch.name for preview_branch in os.scandir(PREVIEW_DIRECTORY / repository_name) if is_preview_branch(preview_branch.path)]

    repository_branches = get_repository_branches(repository_name)

    print(f"De volgende branches bestaan: {repository_branches}")

    for preview_branch in preview_branches:
        if preview_branch not in repository_branches:
            print(f"Kunnen we deleten: {repository_name}/{preview_branch}")
            shutil.rmtree(os.path.join(PREVIEW_DIRECTORY, repository_name, preview_branch))
