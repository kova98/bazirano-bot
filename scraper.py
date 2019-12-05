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
        # Use regex to flter out invalid characters
        match = re.search('^(?:[^\\W\\d_]|)+$', word)
        match_string = ""

        # Append the valid characters to the string
        if (match != None):
            match_string += match.string

        word = match_string.upper()
        
        # One last validation check before adding the word to the keywords list
        if word_valid(word):
            clean.append(word)
    
    return ','.join(clean)

def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Get the main article text div
        tag = soup.find("div", {"class": "text"})

        # Remove the div with ads
        ad = soup.find("div", id="dfp-DIA-container")
        ad.decompose()

        # Get all paragraphs of the article
        paragraphs = tag.find_all('p')
        global paragraphs_text
        paragraphs_text = ""

        # Add all the paragraphs to a single string
        for p in paragraphs:
            paragraphs_text = paragraphs_text + p.text + " "
        
        return paragraphs_text
    except Exception as e:
        print('Error parsing ' + url)
        print(str(e))
        return None

def get_post():
    posts = feedparser.parse(rss_url).entries
    if (posts.__len__() > 0):
        # Get the oldest post from the feed. This is done to avoid duplicates because articles 
        # are oftenly updated just after being published for the first time
        post = posts[posts.__len__() - 1]

        # Get the beginning and end indeces of the image url
        match = re.search("(?<=src=\").*?(?=\")", post['summary'])   
        beginning = match.span()[0]
        end = match.span()[1]

        # Get the guid url and extract the actual guid part from it
        guid = post['guid'] 
        trimmed_guid = guid[guid.find('=') + 1:]

        return {
            "title":post['title'],
            "guid":trimmed_guid,
            "summary":match.string[end+4:],
            "image":match.string[beginning:end],
            "keywords":get_keywords(post['title']),
            "text":get_article_text(post['link'])
        } 

