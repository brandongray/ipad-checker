import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.apple.com/shop/refurbished/ipad"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='page')

e = results.find('div', class_='refurbished-category-grid-no-js')
e.findAll('li')

for ipad in e.findAll('li'):
    ipad_type = ipad.find('a').string
    if re.match('Refurbished iPad Wi-Fi 128GB.*Space Gray.*6th generation', ipad_type):
        print(ipad_type)