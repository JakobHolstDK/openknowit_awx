import requests
import json
import os


# Zabbix API endpoint and credentials
ZABBIX_API_URL = 'https://zabbix.openknowit.com/api_jsonrpc.php'
ZABBIX_USERNAME = os.getenv("ZABBIX_USERNAME")
ZABBIX_PASSWORD = os.getenv("ZABBIX_PASSWORD")
ZABBIX_TOKEN =  os.getenv("ZABBIX_TOKEN")


# Zabbix API authentication payload
auth_payload = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'username': ZABBIX_USERNAME,
        'password': ZABBIX_PASSWORD
    },
    'id': 1,
}

# Authenticate with the Zabbix API
response = requests.post(ZABBIX_API_URL, data=json.dumps(auth_payload), headers={'Content-Type': 'application/json'})
auth_result = response.json()

# Check if authentication is successful
if 'error' in auth_result:
    print(f"Failed to authenticate: {auth_result['error']['data']}")
else:
    print(f"Successfully authenticated. Auth token: {auth_result['result']}")

    # Example: Get hosts from Zabbix
    get_hosts_payload = {
        'jsonrpc': '2.0',
        'method': 'host.get',
        'params': {
            'output': ['hostid', 'host'],
            # You can add more parameters here to filter hosts if needed
        },
        'auth': auth_result['result'],
        'id': 2,
    }

    # Get hosts from Zabbix
    response = requests.post(ZABBIX_API_URL, data=json.dumps(get_hosts_payload), headers={'Content-Type': 'application/json'})
    hosts_result = response.json()
    print(hosts_result)


    # Check if the request was successful
    if 'error' in hosts_result:
        print(f"Failed to get hosts: {hosts_result['error']['data']}")
    else:
        # Print host names and their corresponding host IDs
        for host in hosts_result['result']:
            print(f"Host ID: {host['hostid']}, Host Name: {host['host']}")

# Note: Make sure to handle errors and exceptions properly in a production script.

