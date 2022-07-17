import requests;
from requests.auth import HTTPBasicAuth

GV_CONF_FILE="/opt/cloud/tenants/default/main.tfvars"

def func_read_conf():
    try:
        count = 0
        LV_CONF = open(GV_CONF_FILE, 'r')
        while True:
            count += 1
            LV_LINE = LV_CONF.readline()
            if not LV_LINE:
                break
            print("Line{}: {}".format(count, LV_LINE.strip()))
            # print(LV_LINE)

        LV_CONF.close()

    except FileNotFoundError:
        print("Config file not found or not readable. (/opt/cloud/tenants/default/main.tfvars)")
        exit(2)


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
    func_read_conf()
    func_get_status()

