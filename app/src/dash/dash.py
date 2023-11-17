import redis
from pprint import pprint
import json
import os
import sys
import tempfile
import requests

from .common import prettyllog
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def checkandset_environment():
  runtimeenv = {}
  runtimeenv['ZABBIX_API_URL']      = os.getenv("ZABBIX_API_URL", 'https://zabbix.openknowit.com/api_jsonrpc.php')
  runtimeenv['ZABBIX_API_VERSION']  = os.getenv("ZABBIX_API_VERSION", '2.0')
  runtimeenv['ZABBIX_TOKEN']        = os.getenv("ZABBIX_TOKEN", None)
  runtimeenv['MONGO_HOST']          = os.getenv("MONGO_HOST", 'localhost')
  runtimeenv['MONGO_PORT']          = os.getenv("MONGO_PORT", 27017)
  runtimeenv['MONGO_DB']            = os.getenv("MONGO_DB", 'dash')
  runtimeenv['MONGO_USER']          = os.getenv("MONGO_USER", None)
  runtimeenv['MONGO_PASSWORD']      = os.getenv("MONGO_PASSWORD", None)
  runtimeenv['PG_HOST']             = os.getenv("PG_HOST", 'localhost')
  runtimeenv['PG_PORT']             = os.getenv("PG_PORT", 5432)
  runtimeenv['PG_DB']               = os.getenv("PG_DB", 'dash')
  runtimeenv['PG_USER']             = os.getenv("PG_USER", None)
  runtimeenv['PG_PASSWORD']         = os.getenv("PG_PASSWORD", None)
  runtimeenv['REDIS_HOST']          = os.getenv("REDIS_HOST", 'localhost')
  runtimeenv['REDIS_PORT']          = os.getenv("REDIS_PORT", 6379)
  runtimeenv['REDIS_DB']            = os.getenv("REDIS_DB", 0)
  runtimeenv['REDIS_PASSWORD']      = os.getenv("REDIS_PASSWORD", None)
  return runtimeenv


def get_templateids():
      myenv = checkandset_environment()
      data_payload = {
            "jsonrpc": myenv['ZABBIX_API_VERSION'],
            "method": "template.get",
            "params": {
                                    "output": "['templateid','name']"
                                    },
            "auth": myenv['ZABBIX_TOKEN'],
            "id": 1
            }
      auth_response = requests.post(
            myenv['ZABBIX_API_URL'],
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



def dash():
    print("dash")
    templateids = get_templateids()
    print(templateids)


