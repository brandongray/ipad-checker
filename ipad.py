import requests
from bs4 import BeautifulSoup
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

MATCH_STRING = 'Refurbished iPad Wi-Fi 128GB.*Space Gray.*\(6th Generation\)'

def get_options():
    url = "https://www.apple.com/shop/refurbished/ipad"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='page')

    e = results.find('div', class_='refurbished-category-grid-no-js')
    e.findAll('li')

    matched_ipads = []

    for ipad in e.findAll('li'):
        ipad_type = ipad.find('a').string
        if re.match(MATCH_STRING, ipad_type):
            matched_ipads.append(ipad_type)

    return "\n".join(matched_ipads)

def send_message(message):
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    destinations = os.environ.get("DESTINATIONS")
    from_email = os.environ.get("FROM_EMAIL")

    email_message = Mail(
        from_email=from_email,
        to_emails=destinations,
        subject='iPad',
        html_content=message
    )

    sg.send(email_message)

def send_ipad_options():
    ipads = get_options()

    if ipads:
        print(ipads)
        send_message(ipads)


if __name__ == "__main__":
    send_ipad_options()
