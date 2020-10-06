import os
import re
import sys
import requests
from time import time as timer
from multiprocessing.pool import ThreadPool

def readURLs(filename):
    urls = []
    compiledRegex = re.compile(r"\shttp.*$")
    fileNameRegex = re.compile(r"o\s(.*)\sh")
    file = open(filename, 'r') 
    lines = file.readlines()
    for i in range(1, len(lines)):
        line = lines[i]
        match = fileNameRegex.search(line)
        outputFile = match.group(1)
        match = compiledRegex.search(line)
        url = line[match.start() : match.end()]
        urls.append((url, outputFile))
    return urls

def fetch_url(entry):
    uri, path = entry
    if not os.path.exists(path):
        r = requests.get(uri, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
    return path

if len(sys.argv) != 2:
    print("Usage: python downloadLCs.py <shell script containin curl instructions>")
    exit(1)
start = timer()
urls = readURLs(sys.argv[1])
results = ThreadPool(8).imap_unordered(fetch_url, urls)
for path in results:
    print(path)

print(f"Elapsed Time: {timer() - start}")
