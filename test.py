import requests as r
from lxml import html
import os

url = "https://money.cnn.com/data/markets/nasdaq/"
rtext = "https://money.cnn.com/robots.txt"

page = r.get(url)
robots = r.get(rtext)

print(f"Response code:{page.status_code}")
print(f"Robots code:{robots.status_code}")

if not os.path.exists('robots.txt'):
    with open("robots.txt",'w') as file:
        file.write(robots.text)
if not os.path.exists('page.html'):
    with open("page.html",'w') as file:
        file.write(page.text)



