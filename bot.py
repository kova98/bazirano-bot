import requests
import scraper
import time

URL = "https://localhost:44326/api/postNews"

#posts = scraper.get_posts()
#
#for post in posts:
#    requests.post(URL, json=post, verify=False)

lastPost = scraper.get_post()
firstRun = True

def main_loop():
    global firstRun
    global lastPost
    post = scraper.get_post()
    
    if (post != None):
        if (post != lastPost or firstRun == True):
            lastPost = post
            print(post['title'])

    if (firstRun == True):
        firstRun = False

timer = 5
lastRan = time.mktime(time.localtime())

while(True):
    elapsed = time.mktime(time.localtime()) - lastRan
    if (elapsed > timer):
        lastRan = time.mktime(time.localtime())
        main_loop()