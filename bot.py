import requests
import scraper
import time

URL = "http://localhost/api/postNews"
#URL = "https://localhost:44326/api/postNews"


# posts = scraper.get_posts()

# for post in posts:
#    requests.post(URL, json=post, verify=False)

lastPost = scraper.get_post()
firstRun = True

def main_loop():
    global firstRun
    global lastPost
    post = scraper.get_post()
    
    if (post != None):
        if (post['title'] != lastPost['title'] or firstRun == True):
            if (post['text'] != None):
                lastPost = post
                print(post['title'])
                #requests.post(URL, json=post, verify=False)
        
    if (firstRun == True):
        firstRun = False

while(True):
    main_loop()
    time.sleep(60)