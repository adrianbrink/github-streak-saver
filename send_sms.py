#!/usr/bin/env python

import json
import sys

import requests
from HTMLParser import HTMLParser
from twilio.rest import TwilioRestClient

import conf

class CustomHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "rect":
            self.rects.append(attrs)


def send(s):
    client.sms.messages.create(to=conf.TO, from_=conf.FROM, body=s)

# Use the first arg as the message to send, or use the default if not specified
default_message = "You haven't committed anything today!"
message = sys.argv[1] if len(sys.argv) > 1 else default_message

# Initialise twilio stuff
client = TwilioRestClient(conf.ACCOUNT_SID, conf.AUTH_TOKEN)

# Get Github contributions activity
#url = 'https://github.com/users/%s/contributions_calendar_data' % conf.USERNAME
url = 'https://github.com/users/%s/contributions' % conf.USERNAME
request = requests.get(url)
if request.ok:
    try:
        parser = CustomHTMLParser()
        parser.feed(request.text)

        # Get the last column that signify today's commits
        d = dict(parser.rects[-1])

        # Get the number of commits made today
        comits_today = d["data-count"]

        if comits_today==0:
            send(message)
    except:
        send('There was an error getting the number of commits today')
else:
    send('There was a problem accessing the Github API :(')
