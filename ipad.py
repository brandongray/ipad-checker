import requests
from bs4 import BeautifulSoup
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
destinations = os.environ.get("DESTINATIONS")
from_email = os.environ.get("FROM_EMAIL")

URL = "https://www.apple.com/shop/refurbished/ipad"
page = requests.get(URL)
match_string = 'Refurbished iPad Wi-Fi.*128GB.*Space Gray.*5th generation'

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='page')

e = results.find('div', class_='refurbished-category-grid-no-js')
e.findAll('li')

matched_ipads = []

for ipad in e.findAll('li'):
    ipad_type = ipad.find('a').string
    if re.match(match_string, ipad_type):
        matched_ipads.append(ipad_type)

message = "\n".join(matched_ipads)
print(message)

if message:
    email_message = Mail(
        from_email=from_email,
        to_emails=destinations,
        subject="iPad",
        html_content="\n".join(matched_ipads)
    )

    response = sg.send(email_message)