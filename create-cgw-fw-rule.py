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


# Here we define the function to retrieve the NSX-T Reverse Proxy URL
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


# We need to define all the variables for the compute gateway firewall rule we want to create.
action = ""
destination_group = ""
direction = "IN_OUT"
disabled = False
display_name = ""
ip_protocol = "IPV4_IPV6"
logged = False
scope = ""
services = ""
source_groups = ""
sequence_number = ""

# Like the segment creation, we need to load all of these variables into a JSON payload
json_data = {
    "action": action,
    "destination_group": destination_group,
    "direction": direction,
    "disabled": disabled,
    "display_name": display_name,
    "id": display_name,
    "ip_protocol": ip_protocol,
    "logged": logged,
    "profiles": ["ANY"],
    "resource_type": "Rule",
    "scope": scope,
    "services": services,
    "source_group": source_groups,
    "sequence_number": sequence_number
}

# Now that we have our variables loaded into a JSON payload, we can use a PUT API to create the CGW firewall rule
my_header = {'csp-auth-token': access_token}
my_url = f'{nsx_proxy}/policy/api/v1/infra/domains/cgw/gateway-policies/default/rules/{display_name}'
response = requests.put(my_url, headers=my_header, json=json_data)
json_response = response.json()
if response.status_code == 200:
    print(f'CGW firewall rule {display_name} has been created successfully')
else:
    print("There was an error. Check the syntax.")
    print(f'API call failed with status code {response.status_code}. URL: {my_url}.')
    print(json_response['error_message'])