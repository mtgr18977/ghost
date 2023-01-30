#!/usr/bin/python3
#coding: UTF-8

"""
Links
Return the broken links in Markdown files
"""

__version__ = '0.3.1'   # BETA

# import libraries
from os import listdir, getcwd # read directories and current directory
import urllib.request # make HTTP requests
import re # regular expressions
import textwrap # wraps lines of text at given width


# read the files and folders in the current directory
dirList = listdir(getcwd())
# get the first md file
mdFile = [md for md in dirList if '.md' in md][0]


# get the doc lines
def mdLines(fileName):
    with open(fileName, 'r') as mdFile:
        markdownLines = mdFile.readlines()

    return markdownLines


# get all links, destinations, external links, and namespaces
def linksAndDestinations(lines):
    internalLinksList = []
    internalDestinationList = []
    externalLinksList = []
    nameSpaces = []
    allLinks = []
    allDestinations = []
    allExternalLinks = []
    allNamespaces = []
    for i in range(len(lines)):
        lineInternalLinks = findInternalLinks(lines[i])
        if lineInternalLinks:
            internalLinksList.append([i + 1, lines[i][:-1]])
            for eachLink in lineInternalLinks:
                allLinks.append([i + 1, eachLink[2:-1]])

        lineInternalDestinations = findInternalDestinations(lines[i])
        if lineInternalDestinations:
            internalDestinationList.append([i + 1, lines[i][:-1]])
            allDestinations.append([i + 1, lineInternalDestinations[0][2:-1]])

        lineExternalLinks = findLineExternalLinks(lines[i])
        if lineExternalLinks:
            externalLinksList.append([i + 1, lines[i][:-1]])
            for eachLink in lineExternalLinks:
                allExternalLinks.append([i + 1, eachLink[2:-1]])

        lineNamespaces = findNamespaces(lines[i])
        if lineNamespaces:
            nameSpaces.append([i + 1, lines[i][:-1]])
            for eachNamespace in lineNamespaces:
                allNamespaces.append([i + 1, eachNamespace[2:-1]])

    return [internalLinksList, allLinks, allDestinations, allExternalLinks, allNamespaces]


# get the internal links
def findInternalLinks(line):
    internalLinks = re.findall("\(#[^\)]*\)", line)
    return internalLinks


# get the internal destinations
def findInternalDestinations(line):
    internalDestinations = re.findall("\{#[^\)]*\}", line)
    return internalDestinations


# get the namespaces
def findNamespaces(line):
    internalNamespaces = re.findall("\{%[^\)]*\}", line)
    return internalNamespaces


# get the external links
def findLineExternalLinks(line):
    externalLinks = re.findall("]\(h\S*\S", line)
    return externalLinks 


# each function below prints the elements
def printAllLinks(allLinks):
    for link in allLinks:
        print(f'\033[0m Linha: {link[0]} - Link: (#{link[1]})')


def printAllDestinations(allDestinations):
    for dest in allDestinations:
        print('\033[0m Linha: ' + str(dest[0]) + ' - Destination: {#' + dest[1] + '}')


def printAllNamespaces(allNameSpaces):
    for nameSpace in allNameSpaces:
        if nameSpace[1][-1] == ")":
            nameSpace[1] = nameSpace[1][:-1]
        print('\033[0m Linha: ' + str(nameSpace[0]) + ' - Namespace: ' + '{% ' + str(nameSpace[1]) + '}')


def printAllExternalLinks(allExternalLinks):
    for extLink in allExternalLinks:
        if extLink[1][-1] == ")":
            extLink[1] = extLink[1][:-1]
        print(f'\033[0m Linha: {extLink[0]} - External Link: {extLink[1]}')


# check the broken internal links
def internalLinksChecker(allLinks, allDestinations):
    for link in allLinks:
        flag = False
        for eachDestination in allDestinations:
            if link[1] == eachDestination[1]:
                print(f'\033[92m OK - link in line {link[0]} found in line destination {eachDestination[0]}')
                flag = True
                break
        
        if not flag:
            print(f'\033[91m Line: {link[0]} BROKEN! Check the internal link at (#{link[1]})')


# check the broken external links
def externalLinksChecker(allExternalLinks):
    for link in allExternalLinks:
        try:
            r = urllib.request.urlopen(link[1])
            print(f"\033[92m OK 200 Line: {link[0]} - link: {link[1]}")
        except:
            print(f"\033[91m Line: {link[0]} BAD RESPONSE! Check the external link at {link[1]}")


# check the broken namespaces links
def nameSpacesChecker(allNameSpaces):
    for namespace in allNameSpaces:
        urlNamespace = "https://www.azion.com/"
        coreNamespace = namespace[1][4:-2]
        namespaceParts = coreNamespace.split('_')

        # documentation/products pattern
        if namespaceParts[0] == "documentation" or namespaceParts[0] == "documentacao":
            if namespaceParts[0] == "documentation":
                namespaceLanguage = "en/"
            else:
                namespaceLanguage = "pt-br/"

            urlNamespace += namespaceLanguage + namespaceParts[0] + '/'
            urlNamespace +=  namespaceParts[1] + '/'
            docName = ""
            for i in range(2, len(namespaceParts)):
                docName += namespaceParts[i] + '-'

            docName = docName[:-1]
            urlNamespace += docName + '/'

        # create urlNamespace variable for the other types of patterns
        if namespaceParts[0] == "how":  # it is just an example for how_to
            # TO DO
            pass

        # check the namespace link
        try:
            r = urllib.request.urlopen(urlNamespace)
            print(f"\033[92m Line: {namespace[0]} - namespace link: " + "{%" + namespace[1][:-2] + " %}")
            print(f"\033[92m Equivalent external link: {urlNamespace}\n")
        except:
            print(f"\033[91m Line: {namespace[0]} BAD RESPONSE! Check the namespace link: " + "{%" + namespace[1][:-2] + " %}")
            print(f"\033[92m Equivalent external link: {urlNamespace}\n")


# print the header of the output
def printHeader(lines, mdFile):
    print("\033[0m \n" + "=" * 80)
    print("\n Azion Technologies - Education Team")
    print("\033[0m \n" + "=" * 80)
    print("Documentation file: ", mdFile)
    print(lines[2][:-1])
    print(textwrap.fill(lines[3][:-1], 80))
    
    print("=" * 80)


# starting point of the code - main function
def main():
    lines = mdLines(mdFile)

    printHeader(lines, mdFile)

    linkAndDestinations = linksAndDestinations(lines)
    internalLinksList = linkAndDestinations[0]
    allLinks = linkAndDestinations[1]
    allDestinations = linkAndDestinations[2]
    allExternalLinks = linkAndDestinations[3]
    allNameSpaces = linkAndDestinations[4]

    print(f'Found \33[33m{len(internalLinksList)} lines\033[0m with \33[33m{len(allLinks)} internal links\033[0m in the file \33[33m{mdFile}\033[0m.')
    print(f'Found \33[33m{len(allExternalLinks)} lines\033[0m with \33[33m{len(allExternalLinks)} external links\033[0m in the file \33[33m{mdFile}\033[0m.')
    
    print("=" * 80)

    print('\033[34m \n ' + chr(8730) + ' INTERNAL LINKS\n')
    printAllLinks(allLinks)

    print('\33[95m \n ' + chr(8730) + ' INTERNAL DESTINATIONS\n')
    printAllDestinations(allDestinations)

    print('\33[33m \n ' + chr(8730) + '  EXTERNAL LINKS\n')
    printAllExternalLinks(allExternalLinks)

    print('\33[33m \n ' + chr(8730) + '  NAMESPACES\n')
    printAllNamespaces(allNameSpaces)

    print("\n" + "=" * 80)

    print('\033[34m \n ' + chr(8730) + '  CHECKING INTERNAL LINKS \n')
    internalLinksChecker(allLinks, allDestinations)

    print('\33[33m \n ' + chr(8730) + '  CHECKING EXTERNAL LINKS \n')
    externalLinksChecker(allExternalLinks)

    print('\33[95m \n ' + chr(8730) + '  CHECKING NAMESPACE LINKS \n')
    nameSpacesChecker(allNameSpaces)

    print("\033[0m \n" + "=" * 80 + "\n")


# check if the code is running from itself or was called by another module
if __name__ == '__main__':
    main()
