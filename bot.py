import requests
import scraper
import time
from summarizer import summarize
import summarizer

URL = "http://localhost/api/postNews"
#URL = "https://localhost:44326/api/postNews"

lastPost = scraper.get_post()
firstRun = True

def main_loop():
    global firstRun
    global lastPost
    post = scraper.get_post()

    if (post != None):
        if (post['guid'] != lastPost['guid'] or firstRun == True):
            if (post['text'] != None):
                summarized_text = summarize(post['title'], post['text'], 7)
                post['text'] = "~".join(summarized_text)
                lastPost = post
                print(post['title'])
                requests.post(URL, json=post, verify=False)
        
    if (firstRun == True):
        firstRun = False

while(True):
    main_loop()
    time.sleep(60)