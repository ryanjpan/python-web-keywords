
from urllib2 import urlopen

from bs4 import BeautifulSoup

from collections import Counter

import re
import sys

def word_match(strToCheck, wordList):
    if any(word in strToCheck for word in wordList):
        return True
    else:
        return False

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

class Crawler(object):
    def __init__(self, url):
        self.url = url.strip('\"')
        #find third instance of /
        url = url[url.find("/", url.find("/", url.find("/") + 1) + 1) + 1:]
        words = re.sub("[^\w]", " ",  url).split()
        words = [word.lower() for word in words if len(word) > 4]
        self.urlWords = words

    def crawl(self):
        try:
            soup = BeautifulSoup(urlopen(self.url), "html.parser")
        except:
            print("Could not open URL")
            quit()

        #get text from headers
        headers = soup.find_all(re.compile('^h\d'))
        headers = [header.get_text().encode("ascii").lower() for header in headers]
        if(len(headers) > 0):
            #only get headers with words in URL
            urlMatchedHeaders = [header for header in headers if word_match(header, self.urlWords)]
            #clean the headers
            urlMatchedHeaders = [re.sub("[\n\s]", " ",  header).strip() for header in urlMatchedHeaders]
            if(len(urlMatchedHeaders) > 0):
                for item in urlMatchedHeaders:
                    print(item)
                return

            #If no headers match words in URL
            word = ""
            for header in headers:
                word += " " + header
            counter = Counter(word.split())
            mask = Counter({'a':sys.maxint, 'the':sys.maxint, 'and':sys.maxint, 'to':sys.maxint, 'true':sys.maxint})
            counter.subtract(mask)
            commonWords = counter.most_common(10)
            commonWords = [t[0] for t in commonWords]
            for word in commonWords:
                print(word)
        else:
            #no headers on page
            text = soup.find_all(has_class_but_no_id)
            text = [item.get_text() for item in text]
            text = [re.sub("[^\w]", " ",  item) for item in text]
            word = ""
            for item in text:
                word += " " + item.encode('ascii').lower()
            counter = Counter(word.split())
            mask = Counter({'a':sys.maxint, 'the':sys.maxint, 'and':sys.maxint, 'to':sys.maxint, 'true':sys.maxint})
            counter.subtract(mask);
            commonWords = counter.most_common(10)
            commonWords = [t[0] for t in commonWords]
            print(commonWords)

try:
    crawler = Crawler(sys.argv[1])
except IndexError:
    print("no URL provided")
    quit();
crawler.crawl()
