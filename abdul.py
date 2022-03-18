import re
import requests
import argparse

from os import remove

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to start from")
parser.add_argument("-o", default="word.list", help="Location to save file (default=word.list")
parser.add_argument("-d", type=int, default=2, help="Depth to spider (default=2)")
parser.add_argument("-l", type=int, default=4, help="Minimum length of word to search for (default=4)")
parser.add_argument("-v", help="Display verbose output", action="store_true")

args = parser.parse_args()

class webNode():
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth


def searchContent(data):
    words = re.findall(r"\b\w{%s,15}\b" % args.l,data)
    outFile = open(tempFile,"a", encoding="utf-8")
    wordsToAdd = []
    for word in words:
        word = word.lower()
        if word not in wordsToAdd:
            outFile.write(word+"\n")
            wordsToAdd.append(word)
    outFile.close()


def addURLs(hrefs):
    webListingsStrings = []
    for string in webListings:
        webListingsStrings.append(string.url)
    for urlItem in hrefs:
        newURL = urlItem.replace("href=",'').replace('"','',2)
        if newURL[0] == "/":
            newURL = node.url + newURL # Build URL if it is refrencing a local resource
        if rootDomain in newURL and node.depth < args.d and newURL not in webListingsStrings and not re.match(r'\.(css|zip|gz|bz2|png|gif|jpg|jpeg|bmp|mpg|mpeg|avi|wmv|mov|rm|ram|swf|flv|ogg|webm|mp4|mp3|wav|acc|wma|mid|midi)$',newURL):
            if args.v:
                print("Adding URL: (" + str(len(webListings)) + ") " + newURL)
            webListings.append(webNode(newURL,node.depth+1))
            webListingsStrings.append(newURL)


def dedupeFile():
    print("Starting dedupe")
    outWords = []
    outFile = open(args.o,"a", encoding="utf-8")
    with open(tempFile, encoding="utf-8") as inFile:
        line = inFile.readline()
        while line:
            if line not in outWords:
                outWords.append(line)
                outFile.write(line)
            line = inFile.readline()   
    outFile.close()


webListings = [webNode(args.URL,0)]
rootDomain = re.search(r'\/\/.+\/?',args.URL).group().replace('/','',3)
tempFile = "temp.txt"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

# Loops through each node dynamicaly

if not args.v:
    print("You have chonse no verbose output. This proccess will take a while. You might want to kill this and add \'-v\' to track progress.")
else:
    currentNode = 1

for node in webListings:

    if args.v:
        print("Working on: (" + str(currentNode) + " of " + str(len(webListings)) + ") " + node.url + ":" + str(node.depth))
        currentNode+=1
    
    # Try website connection
    try:
        data = requests.get(node.url,headers=headers)
    except:
        print("Host unreachable:  " + node.url)
        continue
    addURLs(re.findall('href=".+?"',data.text))
    searchContent(data.text)


dedupeFile()
remove(tempFile)