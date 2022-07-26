import sys

import requests
from requests.auth import HTTPBasicAuth
LV_DEBUG = True

def get_vm_status_all(CV_USER, CV_CRED):
    api_url = "https://cloud.skytap.com/v2/configurations.json"

    LV_RES = []
    LV_ITEM = []

    LV_RESP_ROW1 = requests.get(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
    LV_RESP1 = LV_RESP_ROW1.json()
    if LV_RESP_ROW1.status_code != 200:
        print("ERROR, RestAPI return code:" + str(LV_RESP_ROW1.status_code))
        print(LV_RESP1)
        sys.exit(3)

    print('ENV name'.ljust(20, ' ') + '|' + 'HostID'.rjust(10, ' ') + '|' + 'Hostname'.rjust(15,' ') + '|' + 'runstate'.rjust(10, ' ') + '|')
    print('-'.ljust(20, '-') + '|' + '-'.rjust(10, '-') + '|' + '-'.rjust(15,'-') + '|' + '-'.rjust(10, '-') + '|')
    for x in LV_RESP1:
        # print("Check ENV " + str(x['name']) + "...")
        api_url = f"https://cloud.skytap.com/v2/configurations/{str(x['id'])}/vms.json"
        LV_RESP_ROW2 = requests.get(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
        LV_RESP2 = LV_RESP_ROW2.json()
        if LV_RESP_ROW1.status_code != 200:
            print("ERROR, RestAPI return code:" + str(LV_RESP_ROW2.status_code))
            print(LV_RESP2)
            sys.exit(3)
        for y in LV_RESP2:
            print(x['name'].ljust(20, ' ') + '|' + y['id'].rjust(10, ' ') + '|' + y['name'].rjust(15, ' ') + '|' + y['runstate'].rjust(10, ' ') + '|')

    return 0

def get_vm_status(CV_VM_NAME, CV_USER, CV_CRED):
    api_url = "https://cloud.skytap.com/v2/configurations.json"

    LV_RESP_ROW1 = requests.get(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
    LV_RESP1 = LV_RESP_ROW1.json()
    if LV_RESP_ROW1.status_code != 200:
        print("ERROR, RestAPI return code:" + str(LV_RESP_ROW1.status_code))
        print(LV_RESP1)
        sys.exit(3)

    for x in LV_RESP1:
        api_url = f"https://cloud.skytap.com/v2/configurations/{str(x['id'])}/vms.json"
        LV_RESP_ROW2 = requests.get(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
        LV_RESP2 = LV_RESP_ROW2.json()
        if LV_RESP_ROW1.status_code != 200:
            print("ERROR, RestAPI return code:" + str(LV_RESP_ROW2.status_code))
            print(LV_RESP2)
            sys.exit(3)
        for y in LV_RESP2:
            if str.__contains__(str(y['name']), CV_VM_NAME):
                if LV_DEBUG: print("Item: " + str(y['name']) + " id: " + str(y['id']) + ' state:' + str(y['runstate']))
                return [x['id'], y['id'], y['runstate']]

    return 'unknown'


def vm_power(CV_ARGS, CV_USER, CV_CRED, CV_TGT_STATE):
    print('Command: power-' + CV_TGT_STATE + ', HOST: ' + CV_ARGS.target + '...')

    LV_VM = get_vm_status(CV_ARGS.target, CV_USER, CV_CRED)

    # VM_START
    if CV_TGT_STATE == 'on':
        if LV_DEBUG: print('... status: ' + LV_VM[2] + " : try to start...")
        if LV_VM[2].lower() != 'stopped':
            print('ERROR: vm power state is not stopped (' + LV_VM[2] + ')')
            exit(6)

        api_url = f"https://cloud.skytap.com/v2/configurations/{LV_VM[0]}/vms/{LV_VM[1]}.json?runstate=running"

        LV_RESP_ROW = requests.put(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
        LV_RESP = LV_RESP_ROW.json()

        if LV_RESP_ROW.status_code != 200:
            print("ERROR, RestAPI return code:" + str(LV_RESP_ROW.status_code))
            print(LV_RESP)
            sys.exit(3)
        else:
            print("successfully completed code:" + str(LV_RESP_ROW.status_code))
    # VM_STOP
    elif CV_TGT_STATE == 'off':
        if LV_DEBUG: print('... status: ' + LV_VM[2] + " : try to stop...")
        if LV_VM[2].lower() != 'running':
            print('ERROR: vm power state is not running (' + LV_VM[2] + ')')
            exit(6)

        api_url = f"https://cloud.skytap.com/v2/configurations/{LV_VM[0]}/vms/{LV_VM[1]}.json?runstate=halted"

        LV_RESP_ROW = requests.put(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
        LV_RESP = LV_RESP_ROW.json()
        if LV_RESP_ROW.status_code != 200:
            print("ERROR, RestAPI return code:" + str(LV_RESP_ROW.status_code))
            print(LV_RESP)
            sys.exit(3)
        else:
            print("successfully completed code:" + str(LV_RESP_ROW.status_code))

    return True

