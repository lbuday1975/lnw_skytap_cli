import requests
import argparse
import sys

from compute import vm_power, get_vm_status

__version__ = '0.1.0'

from requests.auth import HTTPBasicAuth

GV_CONF_FILE="/opt/cloud/tenants/default/credentials.tfvars"
GV_USER = ""
GV_CRED = ""

GV_AVAILABLE_ACTIONS = [
        'vm_start', 'vm_stop',
        'vm_restart', 'vm_status'
    ]

GV_REQUIRED_PARAMETERS = {
        "vm_start": ["target"],
        "vm_stop": ["target"],
        "vm_restart": ["target"],
        "vm_status": ["target"]
    }


def checkParameters(args, parser):
    if args.version:
        return

    if not "action" in args or not args.action:
        raise parser.error("No action given.")

    if args.action not in GV_AVAILABLE_ACTIONS:
        raise parser.error("Invalid action.")

    if args.action in GV_REQUIRED_PARAMETERS:
        for parameter in GV_REQUIRED_PARAMETERS[args.action]:
            if not parameter in args or getattr(args,parameter) in [None, ""]:
                raise parser.error(f"Parameter --{parameter} is required for action '{args.action}', but has not been provided.")


def func_pars_args():
    print("PARSER")
    LV_PARSER = argparse.ArgumentParser(description=f"LNW-Soft Infrastructure Connector SkyTap {__version__}")
    LV_PARSER.add_argument("--version", action='store_true', help="Show version information")
    LV_PARSER.add_argument("-a", "--action", choices=GV_AVAILABLE_ACTIONS)
    LV_PARSER.add_argument("-t", "--target", help="[vm_*] Target VM")
    LV_ARGS = LV_PARSER.parse_args()

    checkParameters(LV_ARGS, LV_PARSER)

    if LV_ARGS.version:
        print(f"LNW-Soft Infrastructure Connector Azure {__version__}")
        sys.exit(1)
    elif LV_ARGS.action == "vm_start":
        vm_power(LV_ARGS, "on")
    elif LV_ARGS.action == "vm_status":
        print(get_vm_status(LV_ARGS.target, GV_USER, GV_CRED))


def func_read_conf_cred(FV_FILE):
    global GV_CRED
    try:
        count = 0
        LV_CONF = open(FV_FILE, 'r')
        while True:
            count += 1
            LV_LINE = LV_CONF.readline()
            if not LV_LINE:
                break

            if str.__contains__(LV_LINE, "="):
                if str.__contains__(LV_LINE, 'skytap_conn_cred'):
                    LV_VALUE = LV_LINE.split(sep='=')
                    GV_CRED = LV_VALUE[1].replace(' ', '').replace('\n', '').replace('"', '')

        LV_CONF.close()
        return GV_CRED

    except FileNotFoundError:
        print("Config file not found or not readable. (/opt/cloud/tenants/default/credentials.tfvars)")
        exit(2)

def func_read_conf_usr(FV_FILE):
    global GV_USER
    try:
        count = 0
        LV_CONF = open(FV_FILE, 'r')
        while True:
            count += 1
            LV_LINE = LV_CONF.readline()
            if not LV_LINE:
                break

            if str.__contains__(LV_LINE, "="):
                if str.__contains__(LV_LINE, 'skytap_conn_user'):
                    LV_VALUE = LV_LINE.split(sep='=')
                    GV_USER = LV_VALUE[1].replace(' ', '').replace('\n', '').replace('"', '')

        LV_CONF.close()
        return GV_USER

    except FileNotFoundError:
        print("Config file not found or not readable. (/opt/cloud/tenants/default/credentials.tfvars)")
        exit(2)

if __name__ == '__main__':
    GV_USER = func_read_conf_usr(GV_CONF_FILE)
    GV_CRED = func_read_conf_cred(GV_CONF_FILE)
    func_pars_args()
#    func_get_status()

