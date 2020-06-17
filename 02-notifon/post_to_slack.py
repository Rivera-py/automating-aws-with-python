# coding: utf-8

import requests


url = "" # Paste in webhook URL here
data = { "text": "Here is some text!" }

requests.post(url, json=data)
