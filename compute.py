
import requests
from requests.auth import HTTPBasicAuth


def get_vm_status(vm_name, CV_USER, CV_CRED):
    api_url = "https://cloud.skytap.com/v2/configurations.json"

    print("USR:" + CV_USER)
    print("PWD:" + CV_CRED)
    response = requests.get(api_url, auth=HTTPBasicAuth(CV_USER, CV_CRED))
    print("RC:" + str(response.status_code))
    LV_RESP=response.json()

    print("RET111:" + str(LV_RESP))
    print(len(LV_RESP))
    for x in LV_RESP:
        print("Item: " + str(x['name']) + " id: " + str(x['id']))

    return "ONLINE"
#    vm = _get_vm(vm_name)
#    vm_rg = vm.id.split("/")[4]#

#    client = _get_az_client()
#    vm_instance = client.virtual_machines.instance_view(vm_rg, vm_name).as_dict()
#    statuses = vm_instance["statuses"]
#    try:
#        state_dict = list(filter(lambda x: x["code"].startswith("PowerState"), statuses))[0]
#        # e.g. {'code': 'PowerState/running', 'level': 'Info', 'display_status': 'VM running'}
#        power = state_dict["code"].split("/")[1]
#    except:
#        power = "unknown"
#    try:
#        state_dict = list(filter(lambda x: x["code"].startswith("ProvisioningState"), statuses))[0]
#        # e.g. {'code': 'PowerState/running', 'level': 'Info', 'display_status': 'VM running'}
#        provisioning = state_dict["code"].split("/")[1]
#    except:
#        provisioning = "unknown"#
#
#    return {"power": power, "provisioning": provisioning}


def vm_power(args, target_state):
    return True
#    vm = _get_vm(args.target)
#    vm_rg = vm.id.split("/")[4]
#    vm_status = get_vm_status(args.target)#
#
#    client = _get_az_client()
#    if target_state == "on":
#        if vm_status["power"] == "running":
#            print("VM already in target state")
#            return
#        az_action = client.virtual_machines.begin_start(vm_rg, args.target)
#    elif target_state == "off":
#        if  vm_status["power"] == "deallocated":
#            print("VM already in target state")
#            return
#        az_action = client.virtual_machines.begin_deallocate(vm_rg, args.target)
#    elif target_state == "restart":
#        if  vm_status["power"] == "deallocated":
#            # Restart fails on not running machines...
#            # CloudError: Azure Error: OperationNotAllowed
#            # Message: The operation requires the VM to be running (or set to run).
#            az_action = client.virtual_machines.begin_start(vm_rg, args.target)
#        else:
#            az_action = client.virtual_machines.begin_restart(vm_rg, args.target)
#    else:
#        raise NotImplementedError("Action '%s' not implemented" % target_state)
#    az_action.wait()
#    print(az_action.status())
