#!/usr/bin/env python3

import requests                         # need this for Get/Post/Delete
import json

# Initial set of variables to define, so we can get started.
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
    my_header = {'csp-auth-token': access_token}
    my_url = f"https://vmc.vmware.com/vmc/api/orgs/{ORGID}/sddcs/{SDDCID}"
    response = requests.get(my_url, headers=my_header)
    json_response = response.json()
    if response.status_code == 200:
        proxy_url = json_response['resource_config']['nsx_api_public_endpoint_url']
        return proxy_url
    else:
        print("There was an error. Check the syntax.")
        print(f'API call failed with status code {response.status_code}. URL: {my_url}.')
        print(json_response['error_message'])


# Here we are calling the function to retrieve the access token and NSX proxy URL and store them as variables.
access_token = get_access_token(my_token)
nsx_proxy = get_nsxt_proxy(ORGID, SDDCID, access_token)


# Now let's create our segment.  Before we start, we'll need to define a number of additional variables we need to
# create the segment.
segment_name = ""
gateway_address = ""
cidr_range = ""
domain_name = ""
routing_type = ""

# These variables need to be loaded into a JSON payload for the PUT function
json_data = {
    "type": routing_type,
    "display_name": segment_name,
    "id": segment_name,
    "domain_name": domain_name,
    "subnets": [
        {
            "dhcp_ranges": [cidr_range],
            "gateway_address": gateway_address
        }
    ]
}


# Ok, now we need to send this JSON payload to the NSX RP to create the new segment.  We can do this either with a PUT
# or a PATCH.  A PUT will create a new segment and a PATCH will either create a new segment, if it doesn't exist, or
# modify the segment with the matching ID.  A PATCH function is great if you need to modify the connectivity of a
# segment or change the gateway address, etc.
my_header = {'csp-auth-token': access_token}
my_url = f'{nsx_proxy}/policy/api/v1/infra/tier-1s/cgw/segments/{segment_name}'
response = requests.put(my_url, headers=my_header, json=json_data)
json_response = response.json()
if response.status_code == 200:
    print(f'Segment {segment_name} was created successfully')
else:
    print("There was an error. Check the syntax.")
    print(f'API call failed with status code {response.status_code}. URL: {my_url}.')
    print(json_response['error_message'])