#!/usr/bin/env python3

import requests                         # need this for Get/Post/Delete
import json

# These are placed here for convenience - in the real world, one would not embed these values in a script to be redistributed
# Be sure to clear these values before sharing with others.
my_token = ""
ORGID = ""
SDDCID = ""


# Here we have defined the function to retrieve our access token
def get_access_token(my_token):
    params = {'refresh_token': my_token}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    json_response = response.json()
    access_token = json_response['access_token']
    return access_token


# For most things in VMC NSX-T, we're going to work through the NSX Reverse Proxy, not directly with the NSX Manager.
# Working through the NSX RP utilizes the same API, but we need to get that NSX RP URL from another API call.  If we
# have the ORGID and SDDCID, we can return all sorts of information including the NSX RP URL for the SDDC.  We're also
# introducing some error checking here.  If the response from our API doesn't return a HTTP 200 code, we print out the
# error message.  This will aid us in troubleshooting later.
def get_nsxt_proxy(ORGID, SDDCID, access_token):
    myHeader = {'csp-auth-token': access_token}
    myURL = f"https://vmc.vmware.com/vmc/api/orgs/{ORGID}/sddcs/{SDDCID}"
    response = requests.get(myURL, headers=myHeader)
    json_response = response.json()
    if response.status_code == 200:
        proxy_url = json_response['resource_config']['nsx_api_endpoint_url']
        return proxy_url
    else:
        print("There was an error. Check the syntax.")
        print(f'API call failed with status code {response.status_code}. URL: {myURL}.')
        print(json_response['error_message'])


# Here we are calling the function to retrieve the access token and NSX proxy URL and store them as variables.
access_token = get_access_token(my_token)
nsx_proxy = get_nsxt_proxy(ORGID, SDDCID, access_token)


# Now let's create our segment