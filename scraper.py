import feedparser
import re
import requests
from bs4 import BeautifulSoup

rss_url = "https://www.index.hr/rss/vijesti"
postList = []
posts = feedparser.parse(rss_url).entries

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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.find("div", {"class": "text"})
    ad = soup.find("div", id="dfp-DIA-container")
    ad.decompose()
    
    return str(tag)

for post in posts[0:5]:
    match = re.search("(?<=src=\").*?(?=\")", post['summary'])   
    beginning = match.span()[0]
    end = match.span()[1]

    postList.append({
        "title":post['title'],
        "summary":match.string[end+4:],
        "image":match.string[beginning:end],
        "keywords":get_keywords(post['title']),
        "text":get_article_text(post['link'])
        }) 

def get_posts():
    return postList

def get_post():
    if (postList.__len__() > 0):
        return postList[0]

