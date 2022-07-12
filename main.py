import requests;
from requests.auth import HTTPBasicAuth

def func_get_status():
    ##    api_url = "https://10.144.45.42/cloud.skytap.com/v2/configurations/127468724/vms.json?query=vm_name:SAPtest1"

    api_url = "https://cloud.skytap.com/v2/configurations.json"

    response = requests.get(api_url, auth=HTTPBasicAuth('lbuday@lnwsoft.de_227d', 'ed1ac7dd1b4ca3ad1f312777cc7649064e2a2ec8'))
    print("RC:" + str(response.status_code))
    print(type(response.json()))
    LV_RESP=response.json()

    print("RET111:" + str(LV_RESP))
    print(len(LV_RESP))
    for x in LV_RESP:
        print("Item: " + str(x['name']) + " id: " + str(x['id']))


if __name__ == '__main__':
    func_get_status()

