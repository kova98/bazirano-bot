import feedparser
import re
import requests
from bs4 import BeautifulSoup

rss_url = "https://www.index.hr/rss/vijesti"

print('Starting index.hr scraping script...')

def word_valid(word):
    if (len(word) < 4):
        return False
    if (word == "FOTO"):
        return False
    if (word == "VIDEO"):
        return False

    return True

def get_keywords(title):
    words = title.split()
    clean = []

    for word in words:
        match = re.search('^(?:[^\\W\\d_]|)+$', word)
        match_string = ""
        if (match != None):
            match_string += match.string

        word = match_string.upper()
        
        if word_valid(word):
            clean.append(word)
    
    return ','.join(clean)

def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        tag = soup.find("div", {"class": "text"})
        ad = soup.find("div", id="dfp-DIA-container")
        ad.decompose()
        
        return str(tag)
    except:
        print('Error parsing ' + url)
        return None

def get_posts():
    posts = feedparser.parse(rss_url).entries
    for post in posts[0:1]:
        match = re.search("(?<=src=\").*?(?=\")", post['summary'])   
        beginning = match.span()[0]
        end = match.span()[1]

        return {
            "title":post['title'],
            "summary":match.string[end+4:],
            "image":match.string[beginning:end],
            "keywords":get_keywords(post['title']),
            "text":get_article_text(post['link'])
        }

def get_post():
    posts = feedparser.parse(rss_url).entries
    if (posts.__len__() > 0):
        post = posts[0]
        match = re.search("(?<=src=\").*?(?=\")", post['summary'])   
        beginning = match.span()[0]
        end = match.span()[1]

        return {
            "title":post['title'],
            "summary":match.string[end+4:],
            "image":match.string[beginning:end],
            "keywords":get_keywords(post['title']),
            "text":get_article_text(post['link'])
        } 

