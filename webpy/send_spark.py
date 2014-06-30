#!/usr/bin/python

import requests

access_token = "510a78acafff2f5e8183147ee6789c7afe29ec8f"
device_id = "55ff74065075555334280287"

address = 'https://api.spark.io/v1/devices/{0}/update/'.format(device_id)
data = {'access_token': access_token, 'args': '000000000000000'}

r = requests.post(address, data=data)

print(r.text)

