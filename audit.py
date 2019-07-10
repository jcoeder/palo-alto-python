#!/usr/bin/python3

import getpass
import requests
import xmltodict
import datetime
import time
import utils
import threading


# Disable SSL Warnings
requests.urllib3.disable_warnings()


def get_device():
    '''
    Ask user for IP address(es) of device.  Stores device(s) in a list
    '''
    device1 = str(input('IP Address of Primary device.\nPlease use OOB '
                        'management interfaces.\nIP Address: '))
    if device1 == '':
        device1 = None
    device2 = str(input('IP Address of Secondary device.\nPlease use OOB '
                        'management interfaces.\nIf device is a standalone '
                        'device, skip by pressing enter\nIP Address: '))
    if device2 == '':
        device2 = None
    devices = (device1, device2)
    return devices


def palo_alto_api_call(device, cmd, timeout=None, **creditials):
    '''
    Formats and sends an API call to a Palo Alto device.  This function
    can use either basic auth or an API Key.
    '''
    url = 'https://' + device
    cmd = cmd
    url = url + cmd
    params = {'key': creditials['api_key']}
    return requests.get(url, params=params, auth=creditials['auth'], verify=False, timeout=timeout)


def get_system_info():
    '''
    Captures general system information.
    '''
    cmd = '/api/?type=op&cmd=<show><system><info></info></system></show>'
    system_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    return system_info


def get_system_config():
    '''
    '''
    cmd = "/api/?type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"
    system_config = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    return system_config


def get_local_users():
    '''
    '''
    cmd = '/api/?type=config&action=get&xpath=/config/mgt-config/users'
    local_users = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    return local_users


def xml_to_dictionary(xml):
    '''
    Fuction to convert an XML response into a dictionary
    and returns that as a dictionary.
    '''
    return xmltodict.parse(xml.text)


def get_hostname():
    '''
    Using system_info, extract the hostname and print it to the screen.
    '''
    hostname = system_info['response']['result']['system']['hostname']
    print('Hostname : ' + hostname)


def get_system_time():
    '''
    Using system_info, extract the current system time.
    '''
    system_time = system_info['response']['result']['system']['time']
    print('System time : ' + system_time)


def get_dns_servers():
    '''
    Using the system config, extract the DNS servers configuration.
    '''
    dns_servers = system_config['response']['result']['system']['dns-setting']
    print(dns_servers)


device = get_device()[0]
creditials = utils.get_login_creditials()
system_info = get_system_info()
system_config = get_system_config()
local_users = get_local_users()

# Get hostname
threading.Thread(target=get_hostname, name='get_hostname').start()

# Get system time
threading.Thread(target=get_system_time, name='get_system_time').start()

code_version = 'PanOS ' + system_info['response']['result']['system']['sw-version']
print('Code version : ' + code_version)

# Get DNS Servers
threading.Thread(target=get_dns_servers, name='get_dns_servers').start()

print(system_config)
ntp_servers = system_config['response']['result']['system']['ntp-servers']
print(ntp_servers)
