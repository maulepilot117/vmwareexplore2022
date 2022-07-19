#!/usr/bin/env python3

import requests                         # need this for Get/Post/Delete
import json

# These are placed here for convenience - in the real world, one would not embed these values in a script to be redistributed
# Be sure to clear these values before sharing with others.
my_token = ""

# Now we are just defining a function to perform the same thing we did in the last example... this will allow us to call it whenever we want.
def get_access_token(my_token):
    params = {'refresh_token': my_token}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token

# Here we are calling the function to retrieve the access token and store it as a variable.
access_token = get_access_token(my_token)

# Based on the API URL, we need to supply a couple additional pieces of information - first, the ORG ID:
org_id = ""

# We must also provide the ID of the group to add users to... we are using the python "input" method to request user input:
group_id = input("Please type in the group ID to add the user to: ")

# Finally, we have to request the email address of the user to add to the group:
users = input("Please type in the email of the user to add: ")

# Below we build a JSON payload to provide the necessary information to the API...
# See https://developer.vmware.com/apis/csp/csp-iam/latest/csp/gateway/am/api/orgs/orgId/groups/groupId/users/post/ for more information
payload = {
        'notifyUsers': 'false',
        'usernamesToAdd': [users]
        }

myHeader = {'csp-auth-token': access_token, 'Content-Type': 'application/json'}
myURL = f'https://console.cloud.vmware.com/csp/gateway/am/api/orgs/{org_id}/groups/{group_id}/users'

response = requests.post(myURL, data =json.dumps(payload), headers = myHeader)
json_response = response.json()

print(" ")
print(f"Added: {json_response['succeeded']}" )
print(f"Failed: {json_response['failed']}" )
