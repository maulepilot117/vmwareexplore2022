import requests                         # need this for Get/Post/Delete
import json
from prettytable import PrettyTable

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


# Retrieving information is just a GET request, so we'll send a GET request to the API for the NSX T0 route table
my_header = {'csp-auth-token': access_token}
my_url = f'{nsx_proxy}/policy/api/v1/infra/tier-0s/vmc/routing-table?enforcement_point_path=/infra/sites/default/enforcement-points/vmc-enforcementpoint'
response = requests.get(my_url, headers=my_header)
json_response = response.json()
if response.status_code == 200:
    t0_routes = json_response['results'][1]['route_entries']
    print(t0_routes)

    # pretty_data = json.dumps(json_response, indent=4)
    # print(pretty_data)

    # route_table = PrettyTable(['Route Type', 'Network', 'Admin Distance', 'Next Hop'])
    # for routes in t0_routes:
    #     route_table.add_row([routes['route_type'], routes['network'], routes['admin_distance'], routes['next_hop']])
    # print('T0 Routes')
    # print('Route Type Legend:')
    # print(
    #     't0c - Tier-0 Connected\nt0s - Tier-0 Static\nb   - BGP\nt0n - Tier-0 NAT\nt1s - Tier-1 Static\nt1c - Tier-1 Connected\nisr: Inter-SR')
    # print(route_table.get_string(sort_key=operator.itemgetter(1, 0), sortby="Network", reversesort=True))

else:
    print("There was an error. Check the syntax.")
    print(f'API call failed with status code {response.status_code}. URL: {my_url}.')
    print(json_response['error_message'])
