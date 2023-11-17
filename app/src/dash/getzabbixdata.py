#!/usr/bin/env python3

import requests
import json
import random
import os
import redis

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

r = redis.Redis(host='localhost', port=6379, db=0)



ZABBIX_API_URL =  os.getenv("ZABBIX_API_URL")
if ZABBIX_API_URL is None:
      print("ZABBIX_API_URL is not set")
      exit(1)

ZABBIX_API_TOKEN = os.getenv("ZABBIX_TOKEN")
if ZABBIX_API_TOKEN is None:
      print("ZABBIX_TOKEN is not set")
      exit(1)

ZABBIX_API_METHOD = "item.get"
ZABBIX_API_VERSION = "2.0"  # Change this to match your Zabbix version

def get_templateids():
      data_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": "template.get",
            "params": {
                                    "output": "['templateid','name']"
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(data_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )
# Check the response

      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)



def get_hostids():
      data_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": "host.get",
            "params": {
                                    "output": "['hostid','name']"
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(data_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )
# Check the response
      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)


      

def get_itemids():
      data_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": ZABBIX_API_METHOD,
            "params": {
                                    "output": "['itemid','name','key_','lastvalue']"
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }


# Disable SSL certificate verification (trust self-signed cert)
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(data_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )
# Check the response
      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)
def get_templateid_details(templateid):
      details_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": "template.get",
            "params": {
                                    "output": "extend",
                                    "filter": {
                                          "templateid": templateid
                                          }
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
      # Disable SSL certificate verification (trust self-signed cert)
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(details_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )
      
# Check the response
      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)

def get_hostid_details(hostid):
      details_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": "host.get",
            "params": {
                                    "output": "extend",
                                    "filter": {
                                          "hostid": hostid
                                          }
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
      # Disable SSL certificate verification (trust self-signed cert)
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(details_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )
      
# Check the response
      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)

def get_itemid_details(itemid):
      details_payload = {
            "jsonrpc": ZABBIX_API_VERSION,
            "method": "item.get",
            "params": {
                                    "output": "extend",
                                    "filter": {
                                          "itemid": itemid
                                          }
                                    },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
      # Disable SSL certificate verification (trust self-signed cert)
      auth_response = requests.post(
            ZABBIX_API_URL,
            data=json.dumps(details_payload),
            headers={"Content-Type": "application/json"},
            verify=False  # This line disables SSL certificate verification
            )

# Check the response
      if auth_response.status_code == 200:
            data_result = auth_response.json()
            return data_result['result']
      else:
            print(f"Failed to connect to Zabbix API. Status Code: {auth_response.status_code}")
            exit(1)





def main():
      templateids = get_templateids()
      nbr_templates = len(templateids)
      templatenbr = 1
      templatecached = 0
      templateadded = 0
      for template in templateids:
            if r.exists(str(template)):
                  #suppress newline when printing
                  print("(%06d/%06d/%06d/%06d) Template already exists %-20s " % ( templatenbr, templatecached, templateadded , nbr_templates, template))
                  templatecached = templatecached + 1
            else:
                  templatedetails = get_templateid_details(template)
                  print(templatedetails)
                  delay = random.randint(240000, 420000)
                  r.set(str(template), "True", ex=delay)
                  templateadded = templateadded + 1
                  print("(%06d/%06d/%06d/%06d) Template added to redis %-20s " % ( templatenbr, templatecached, templateadded , nbr_templates, template))
            templatenbr = templatenbr + 1
            
      hostids = get_hostids()
      nbr_hosts = len(hostids)
      hostnbr = 1
      hostcached = 0
      hostadded = 0
      for host in hostids:
            if r.exists(str(host)):
                  print("(%06d/%06d/%06d/%06d) Host already exists %-20s " % ( hostnbr, hostcached, hostadded , nbr_hosts, host))
                  hostcached = hostcached + 1

            else:
                  #hostdetails = get_hostid_details(host)
                  delay = random.randint(24000, 42000)
                  r.set(str(host) , "True", ex=delay)
                  hostadded = hostadded + 1
                  print("(%06d/%06d/%06d/%06d) Host added to redis %-20s " % ( hostnbr, hostcached, hostadded , nbr_hosts, host))

            hostnbr = hostnbr + 1
            

      itemids = get_itemids()
      nbr_items = len(itemids)
      itemnbr = 1
      itemcached = 0
      itemadded = 0
      for item in itemids:
            if r.exists(str(item)):
                  print("(%06d/%06d/%06d/%06d) Item already exists %-20s " % ( itemnbr, itemcached, itemadded , nbr_items, item))
                  itemcached = itemcached + 1

            else:
                  #itemdetails = get_itemid_details(item)
                  delay = random.randint(24000, 42000)
                  r.set(str(item) , "True", ex=delay)
                  itemadded = itemadded + 1
                  print("(%06d/%06d/%06d/%06d) Item added to redis %-20s " % ( itemnbr, itemcached, itemadded , nbr_items, item))

            itemnbr = itemnbr + 1



if __name__ == "__main__":
      main()


