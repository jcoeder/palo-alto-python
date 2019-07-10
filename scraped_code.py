def number_of_admins_logged_in(ip_address, api_key):
    '''
    Retrieves the number of admins logged into a single device.
    Input is an IP Address and API Key

    The API command returns the following XML in which each 'entry name' is an
    administrator that is currently logged in. 

<response status="success">
  <result>
    <admins>
      <entry name="admin"/>
      <entry name="api"/>
      <entry name="panorama"/>
    </admins>
  </result>
</response>
    '''
    api_call = 'https://{}/api/?type=op&cmd=<show><admins><all></all></admins></show>&key={}'.format(ip_address, api_key)
    response = requests.get(api_call, verify=False, timeout=20)
    response = response.text
    dictionary_response = xmltodict.parse(response)
    number_of_admins_logged_in = 0
    for entry in dictionary_response['response']['result']['admins']['entry']:
        number_of_admins_logged_in = number_of_admins_logged_in + 1
    return number_of_admins_logged_in

def number_of_admins_logged_in_ha_pair(primary_device, secondary_device):
    '''
    Returns the number of admins logged into an HA pair as a dictionary.
    Format is {'device1': number_of_admins, 'device2': number_of_admins}
    '''
    number_of_admins_logged_in_ha_pair = {'primary_device': number_of_admins_logged_in(primary_device), 'secondary_device': number_of_admins_logged_in(secondary_device)}
    return number_of_admins_logged_in_ha_pair

def are_other_users_logged_in(number_of_admins_logged_in_ha_pair):
    '''
    Checks to see if more than or less than one admin is logged into
    each device.  This one admin should be the user making the call.
    Returns True if only one admin on each device
    '''
    if number_of_admins_logged_in_ha_pair['primary_device'] == number_of_admins_logged_in_ha_pair['secondary_device'] == 1:
        return True
    else:
        return False