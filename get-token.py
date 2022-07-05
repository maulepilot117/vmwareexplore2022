#!/usr/bin/env python3

import requests                         # need this for Get/Post/Delete
import json

# These are placed here for convenience - in the real world, one would not embed these values in a script to be redistributed
# Be sure to clear these values before sharing with others.
my_token = ""

"""
How would you handle these values instead?  
See the following for some examples:
https://flings.vmware.com/sddc-import-export-for-vmware-cloud-on-aws
https://flings.vmware.com/python-client-for-vmc-on-aws
"""


""" Gets the Access Token using the Refresh Token.  See the following site for more information - https://developer.vmware.com/apis/vmc/latest/"""
params = {'refresh_token': my_token}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
# response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', headers=headers)
# print(response)
json_response = response.json()
# print(json.dumps(json_response, indent = 2))
access_token = json_response['access_token']
print(access_token)