#!/usr/bin/python3

import getpass
import requests
import xmltodict
import datetime
import time
import utils

# Disable SSL Warnings
requests.urllib3.disable_warnings()


def get_login_creditials():
    '''
    Collects login information from the user.  If a blank string is provided
    the type is set to None.  Returns a dictionary of all the information
    supplied.  Used later as **kwargs for the palo_alto_api_call function.
    Should continue to ask user until either a username and password or
    API key are provided.  Unprovided values are set to None.  The
    requests library generally skips over None values.
    '''

    while True:
        # Request username, store username as username.  If blank string or
        # no entry is provided, set to None.
        username = str(input('Username: '))
        if username == '':
            username = None

        # Request password, store password as password.  If blank string or
        # no entry is provided, set to None.
        password = getpass.getpass()
        if password == '':
            password = None

        # Request API Key, store API Key as api_key.  If blank string or
        # no entry is provided, set to None.
        if password != None:
            api_key = None
        elif password == None:
            api_key = str(input('API Key: '))
            if api_key == '':
                api_key = None

        # Create auth object.  If username or password is None object should
        # be None.  If both username and password are provided auth should
        # be a list of (username, password)
        if username == None or password == None:
            auth = None
        else:
            auth = (username, password)

        if (username != None and password != None) or api_key != None:
            # Create dictionary for **kwargs use later.  We store these entries
            # in a dictionary so we can pass them to functions and call the
            # specifc keys needed in each fuction.
            creditials = {
                'auth': auth,
                'api_key': api_key
                }
            return creditials

        print('Please provide either username and',\
              'password combination or API Key.')


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


def xml_to_dictionary(xml):
    '''
    Fuction to convert an XML response into a dictionary
    and returns that as a dictionary.
    '''
    return xmltodict.parse(xml.text)


def reboot():
    '''
    API command for reboot will usually timeout.  We need to silenly pass the timeout.
    '''
    print('\nDevice is rebooting.\n')
    cmd = '/api/?type=op&cmd=<request><restart><system></system></restart></request>'
    try:
        palo_alto_api_call(device, cmd, **creditials, timeout=5)
    except requests.exceptions.ReadTimeout:
        pass
    else:
        pass


def wait_for_shutdown():
    '''
    Physical devices take a measureable amount of time to stop all services.
    We must wait for these services to stop before we can begin to check if
    the device has rebooted otherwise we may have a false positive.
    '''
    x = 90
    while x > 0:
        time.sleep(1)
        x = x-1
        print('***** Waiting ' + str(x) + ' seconds while device ' \
              'shuts down services for reboot. *****\r', end='')
    print('                                            ', \
          '                                            ', end='\r', flush=True)


def check_if_device_booted():
    '''
    During the boot process the firewalls goes through a series of stages
    where the web server may return a variety of errors if attempted to
    be accessed before fully booted.  We can assume the device is fully
    booted if we can run an API call and get a 200 response.
    '''
    start_time = time.time()
    while True:
        time.sleep(2)
        try:
            cmd = '/api/?type=op&cmd=<show><system><info></info></system></show>'
            response = palo_alto_api_call(device, cmd, **creditials)
            if response.status_code == 200:
                print('\nDevice has booted')
                break
            elif response.status_code != 200:
                response.raise_for_status()
                pass
        except requests.exceptions.RequestException:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.HTTPError:
            pass
        print('***** Waiting for device to boot. Wait time: ' + str(time.time() - start_time) + ' *****\r', end='')


def bordered_text(text):
    '''
    Prints a box around text.
    '''
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
