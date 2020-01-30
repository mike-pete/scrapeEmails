# Author: Mike Peterson
# Date: 1/31/2020
#
# This is a command line tool that scrapes user specified 
# websites and dumps a list of emails found on those sites.
# 
# usage: python main.py http://example.com

import sys          # capture argv
import requests     # web requests
import re           # regular expressions (regex)

emailsByUrl = {}


# scrape website and return a list of emails found
# return True if everything went smoothly
def getEmails(url):
    try:
        site = requests.get(url).content.decode('utf-8')    # get site
        reg = re.compile('[\w\d\.]+@[\w\d\.]+\.[\w]{2,}')   # set regex to use

        # add url to emailsByUrl
        if url not in emailsByUrl:
            emailsByUrl[url] = []

        # add emails
        for email in reg.findall(site):
            if email not in emailsByUrl[url]:
                emailsByUrl[url].append(email)

    except:
        print(f'There was an issue scraping "{url}"')
        print('Usage: python main.py http://example.com')
        return False
    return True


def printEmailsFound():
    totalEmailCount = 0
    print('')
    for url in emailsByUrl:
        emails = emailsByUrl[url]
        totalEmailCount += len(emails)
        print(f'{url} ({len(emails)} found):\n ', end='')
        print('\n '.join(emails),'\n\n')
    
    print(f'Total Found: {totalEmailCount}')


# get a list of urls by looping through argv
# skip argv[0] because it's the filename
for i in range(1, len(sys.argv)):
    url = sys.argv[i]
    if getEmails(url):
        printEmailsFound()
