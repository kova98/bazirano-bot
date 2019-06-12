import requests
import scraper

URL = "https://localhost:44326/api/postNews"

posts = scraper.get_posts()

for post in posts:
    requests.post(URL, json=post, verify=False)