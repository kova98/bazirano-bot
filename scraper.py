import feedparser
import re

rss_url = "https://www.index.hr/rss/vijesti"
postList = []
posts = feedparser.parse(rss_url).entries

for post in posts:
    title = post['title']

    summary = post['summary']
    match = re.search("(?<=src=\").*?(?=\")", summary)   
    beginning = match.span()[0]
    end = match.span()[1]

    image = match.string[beginning:end]
    text = match.string[end+4:]    

    postList.append({
        "title":title,
        "text":text,
        "image":image
        })

def get_posts():
    return postList

