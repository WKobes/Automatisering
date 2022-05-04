import os
import shutil


def getValue(var, line):
    start = line.find("\"") + 1
    end = line.find("\",")
    val = line[start:end]
    print(f"{var}: {val}")
    return val


content = "content"
config = f"{content}/js/config.js"
f = open(config, "r", encoding="utf-8")

pubDomain = ""
shortName = ""
publishVersion = ""

for line in f:
    if "pubDomain" in line:
        pubDomain = getValue("pubDomain", line)
    elif "shortName" in line:
        shortName = getValue("shortName", line)
    elif "publishVersion" in line:
        publishVersion = getValue("publishVersion", line)

f.close()
os.remove(config)

if len(pubDomain) * len(shortName) > 0:
    try:
        if len(publishVersion) > 0:
            shutil.copytree(content, f"{content}/{publishVersion}")
        path = f"publicatie/{pubDomain}/{shortName}/"
        for fn in os.listdir(path):
            # https://stackoverflow.com/a/185941
            file_path = os.path.join(path, fn)
            try:
                print("file_path: " + file_path)
                if os.path.isdir(file_path):
                    files = os.listdir(file_path)
                    if "index.html" in files and fn != publishVersion:
                        shutil.copytree(file_path, f"{content}/{fn}")
            except Exception as e:
                print(e)
        shutil.rmtree(path)
        print("Cleared dir: " + path)
        shutil.copytree(content, path)
        print("Created dir: " + path)
    except Exception as e:
        print(e)
