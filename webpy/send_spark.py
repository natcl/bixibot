#!/usr/bin/python

import requests

access_token = 'xxxx'
device_id = 'xxxx'

address = 'https://api.spark.io/v1/devices/{0}/update/'.format(device_id)
data = {'access_token': access_token, 'args': '000000000000000'}

r = requests.post(address, data=data)

print(r.text)

