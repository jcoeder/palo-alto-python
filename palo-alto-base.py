def which_api_admin(ip_address, api_key):
    '''
    Uses the API Key to log into a device.  Device will return XML looking like
    the following.  Depending on how many admins are logged in XML will vary
    as well as the xmltodict parsing.  The admin with 'idle-for' equal to '00:00:00s'
    and a 'type' equal to 'Web' is the admin we are logged in with.  We want to
    know this to determine if we are the only admin logged in or not

    Single admin Logged In

    <response status="success">
      <result>
        <admins>
          <entry>
            <admin>api</admin>
            <from>172.31.88.30</from>
            <type>Web</type>x
            <session-start>12/08 18:42:48</session-start>
            <idle-for>00:00:00s</idle-for>
          </entry>
        </admins>
      </result>
    </response>

    Returns - ['api']


    Multiple admins Logged In

    <response status="success">
      <result>
        <admins>
          <entry>
            <admin>api</admin>
            <from>172.31.88.30</from>
            <type>Web</type>
            <session-start>12/08 18:42:48</session-start>
            <idle-for>00:00:00s</idle-for>
          </entry>
          <entry>
            <admin>admin</admin>
            <from>172.31.88.30</from>
            <type>CLI</type>
            <session-start>12/09 11:59:23</session-start>
            <idle-for>00:18:30s</idle-for>
          </entry>
        </admins>
      </result>
    </response>

    Returns - ['api']
    '''
    api_call = 'https://{}/api/?type=op&cmd=<show><admins></admins></show>&key={}'.format(ip_address, api_key)
    dictionary_response = requests_response_to_dictionary(api_call)
    dictionary_response = dictionary_response['response']['result']['admins']['entry']
    list_api_admin =[]
    if isinstance(dictionary_response, list) == True:
        count = 0
        for entry in dictionary_response:
            if entry['type'] == 'Web' and entry['idle-for'] == '00:00:00s':
                api_admin = dictionary_response[count]['admin']
                list_api_admin.append(api_admin)
                return list_api_admin
            else:
                exit()
            count +=1
    elif isinstance(dictionary_response, dict) == True:
        if dictionary_response['type'] == 'Web' and dictionary_response['idle-for'] == '00:00:00s':
            api_admin = dictionary_response['admin']
            list_api_admin.append(api_admin)
            return list_api_admin
        else:
            exit()
    else:
        exit()


def only_admin_logged_in(ip_address, api_key, ha_info):
    '''
    Depending on the type of device(s).  This function checks to see if the
    api_admin we are logging in with is the only admin logged in to either
    device, if a cluster, or the singlular device if it is stand-alone.
    '''
    if get_ha_mode(ha_info) == 'Active-Passive':
        active_device = get_active_device(ha_info)
        passive_device = get_passive_device(ha_info)
        if admins_logged_in(active_device, api_key) == which_api_admin(active_device, api_key) and admins_logged_in(passive_device, api_key) == which_api_admin(passive_device, api_key):
            print('Active-Passive - api_admin is the only admin logged in.')
            pass
        else:
            print('Active-Passive - Other admins are logged in.')
            print(str(admins_logged_in(active_device, api_key)) + ' are currently logged into the Active Device')
            print(str(admins_logged_in(passive_device, api_key)) + ' are currently logged into the Passive Device')
    elif get_ha_mode(ha_info) == 'Active-Active':
        primary_device = get_primary_device(ha_info)
        secondary_device = get_secondary_device(ha_info)
        if admins_logged_in(primary_device, api_key) == which_api_admin(primary_device, api_key) and admins_logged_in(secondary_device, api_key) == which_api_admin(secondary_device, api_key):
            print('Active-Active - api_admin is the only admin logged in.')
            pass
        else:
            print('Active-Active - Other admins are logged in.')
            print(str(admins_logged_in(primary_device, api_key)) + ' are currently logged into the Primary Device')
            print(str(admins_logged_in(secondary_device, api_key)) + ' are currently logged into the Secondary Device')
    elif get_ha_mode(ha_info) == 'Stand-Alone':
        if admins_logged_in(ip_address, api_key) == which_api_admin(ip_address, api_key):
            print('Stand Alone - api_admin is the only admin logged in.')
            pass
        else:
            print('Stand Alone - Other admins are logged in.')
            print(str(admins_logged_in(ip_address, api_key)) + ' are currently logged in')


def admins_logged_in(ip_address, api_key):
    '''
    Returns a list of all of the admins logged in.  xmltodict
    provides only a dictionary if a single admin is logged in
    but provides a list of dictionaries if multiple admins are
    logged in.  To work around this we must use isinstance to
    validate what data is being provided.

    Single Admin Logged In

    <response status="success">
      <result>
        <admins>
          <entry>
            <admin>api</admin>
            <from>172.31.88.30</from>
            <type>Web</type>
            <session-start>12/08 18:42:48</session-start>
            <idle-for>00:00:00s</idle-for>
          </entry>
        </admins>
      </result>
    </response>

    Returns - ['api']


    Multiple Admins Logged In

    <response status="success">
      <result>
        <admins>
          <entry>
            <admin>api</admin>
            <from>172.31.88.30</from>
            <type>Web</type>
            <session-start>12/08 18:42:48</session-start>
            <idle-for>00:00:00s</idle-for>
          </entry>
          <entry>
            <admin>admin</admin>
            <from>172.31.88.30</from>
            <type>CLI</type>
            <session-start>12/09 11:59:23</session-start>
            <idle-for>00:18:30s</idle-for>
          </entry>
        </admins>
      </result>
    </response>

    Returns - ['api', 'admin']
    '''
    api_call = 'https://{}/api/?type=op&cmd=<show><admins></admins></show>&key={}'.format(ip_address, api_key)
    dictionary_response = requests_response_to_dictionary(api_call)
    instance_test = dictionary_response['response']['result']['admins']['entry']
    list_of_admins = []
    if isinstance(instance_test, dict):
        admins = dictionary_response['response']['result']['admins']['entry']['admin']
        list_of_admins.append(admins)
        return list_of_admins
    elif isinstance(instance_test, list):
        for admin in dictionary_response['response']['result']['admins']['entry']:
            list_of_admins.append(admin['admin'])
        return list_of_admins


def get_device_serial_number(device, api_key):
    '''
    Given a device hostname or IP address returns the
    device serial number as a string.
    '''
    api_call = 'https://{}/api/?type=op&cmd=<show><system><info></info></system></show>&key={}'.format(device, api_key)
    dictionary_response = requests_response_to_dictionary(api_call)
    serial_number = dictionary_response['response']['result']['system']['serial']
    return str(serial_number)


def backup_config(device, api_key):
    '''
    Pulls the current running and saved XML configuraiton
    and writes it to a file.  File format is:
    <device_serial>-<date-time>.xml
    '''
    api_call = 'https://{}/api/?type=export&category=configuration&key={}'.format(device, api_key)
    device_serial = get_device_serial_number(device, api_key)
    device_configuration_backup = requests.get(api_call, verify=False, timeout=20)
    device_configuration_backup = device_configuration_backup.text
    device_configuration_backup_file = open(device_serial + '-' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.xml', 'w')
    device_configuration_backup_file.write(device_configuration_backup)


def backup_running_configuration(ip_address, api_key, ha_info):
    if get_ha_mode(ha_info) == 'Active-Passive':
        active_device = get_active_device(ha_info)
        passive_device = get_passive_device(ha_info)
        backup_config(active_device, api_key)
        backup_config(passive_device, api_key)
        print('Backed up Active-Passive firewall pair')
    elif get_ha_mode(ha_info) == 'Active-Active':
        primary_device = get_primary_device(ha_info)
        secondary_device = get_secondary_device(ha_info)
        backup_config(primary_device, api_key)
        backup_config(secondary_device, api_key)
        print('Backed up Active-Active firewall pair')
    elif get_ha_mode(ha_info) == 'Stand-Alone':
        backup_config(ip_address, api_key)
        print('Backed up Stand-Alone firewall')
    else:
        print('ha is funky')


def update_firewall_license(primary_device, secondary_device, api_key):
    devices = (primary_device, secondary_device)
    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><license><fetch></fetch>\
        </license></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)
        response = response.status_code
        status = []
        status = status.append(response)
        if status [0] == status [1] and status[1]  == 200:
            return True
        else:
            return False


def check_url_compat(ha_info):
    if ha_info['response']['result']['group']['local-info']['url-compat'] == 'Mismatch':
        print('url-compat mismatch')
        exit()
    elif ha_info['response']['result']['group']['local-info']['url-compat'] == 'Match':
        pass
    else:
        print('other url-compat failure')
        exit()


def check_av_compat(ha_info):
    if ha_info['response']['result']['group']['local-info']['av-compat'] == 'Mismatch':
        print('av-compat mismatch')
        exit()
    elif ha_info['response']['result']['group']['local-info']['av-compat'] == 'Match':
        pass
    else:
        print('other av-compat failure')
        exit()


def check_vpnclient_compat(ha_info):
    if ha_info['response']['result']['group']['local-info']['vpnclient-compat'] == 'Mismatch':
        print('url-compat mismatch')
        exit()
    elif ha_info['response']['result']['group']['local-info']['vpnclient-compat'] == 'Match':
        pass
    else:
        print('other vpnclient-compat failure')
        exit()

def check_running_sync(ha_info):
    if ha_info['response']['result']['group']['running-sync'] == 'synchronized':
        print('Running configuration is synchronized between devices')
        pass
    elif ha_info['response']['result']['group']['running-sync'] == 'synchronization in progress':
        print('Running configuration in the process of synchronizing between devices')
        print('Please wait and try again')
    elif ha_info['response']['result']['group']['running-sync'] == 'not synchronized':
        print('Running configuration is NOT synchronized between devices')
    else:
        print('config sync is funky')

def check_ha_status(ha_info):
    if ha_info['response']['result']['group']['peer-info']['conn-status'] == 'up':
        print('conn-status up')
    elif ha_info['response']['result']['group']['peer-info']['conn-status'] == 'down':
        print('conn-status down')
    else:
        print('ha status is funky')

def get_job_id (dicationary_response):
    job_id = dictionary_response['response status']['result']['job']
    return job_id

def wait_for_job_finish(device, job_id, api_key):
    '''
    Every 15 seconds checks for the status of the provided job
    Returns True if job finishes with status FIN and result OK
    Returns False on a 15 minute timeout
    Returns False if result FAIL
    '''
    timeout = time.time() + 60*15  #15 minutes
    while True:
        api_call = 'https://{}/api/?type=op&cmd=<show><jobs><id>{}</id></jobs></show>&key={}'.format(device, job_id, api_key)
        dictionary_response = requests_response_to_dictionary(api_call)
        job_status = dictionary_response['response_status']['result']['job']['status']
        job_result = dictionary_response['response_status']['result']['job']['result']
        if job_status == 'FIN' and job_result == 'OK':
            return True
        elif job_result == 'FAIL':
            return False
        elif time.time() >= timeout:
            return False
        else:
            time.sleep(15)

def upgrade_anti_virus(active_device, passive_device, api_key):
    '''
    Connects to both firewalls in a HA pair.  Downloads and
    Installs the 'latest' anti virus definitions.
    Times out after 15 minutes.
    '''
    devices = (active_device, passive_device)
    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><anti-virus><upgrade><download><latest></latest></download></upgrade></anti-virus></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)
        response = response.text
        dictionary_response = xmltodict.parse(response)
        job_id = get_job_id(dictionary_response)
        job_status = wait_for_job_finish(job_id)
        if job_status is True:
            continue
        elif job_status is False:
            break

    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><anti-virus><upgrade><install><version>latest</version></install></upgrade></anti-virus></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)
        response = response.text
        dictionary_response = xmltodict.parse(response)
        job_id = get_job_id(dictionary_response)
        job_status = wait_for_job_finish(job_id)
        if job_status is True:
            return True
        elif job_status is False:
            return False

#Downloads latest
#2018-09-18 13:58:33
#<response status="success" code="19"><result><msg><line>Download job enqueued with jobid 7708</line></msg><job>7708</job><
#/result></response>

#Downloaded
#<response status="success"><result><job><tenq>2018/09/18 14:02:13</tenq><tdeq>14:02:13</tdeq><id>7710</id><admin/><type>Downld</type><status>FIN</status><queued>NO</queued><stoppable>no</stoppable><result>OK</result><tfin>14:02:21</tfin><description/><positionInQ>0</positionInQ><progress>14:02:21</progress><details><line>File successfully downloaded
#</line></details><warnings/></job></result></response>

#downloading
#<response status="success"><result><job><tenq>2018/09/18 14:07:58</tenq><tdeq>14:07:58</tdeq><id>7712</id><admin/><type>Downld</type><status>ACT</status><queued>NO</queued><stoppable>yes</stoppable><result>PEND</result><tfin>Still Active</tfin><description/><positionInQ>0</positionInQ><progress>13</progress><details/><warnings/></job></result></response>

#Get and check job ID... Eventually add that logic

#installing
#<response status="success"><result><job><tenq>2018/09/18 14:09:18</tenq><tdeq>14:09:18</tdeq><id>7713</id><admin/><type>Antivirus</type><status>ACT</status><queued>NO</queued><stoppable>no</stoppable><result>PEND</result><tfin>Still Active</tfin><description/><positionInQ>0</positionInQ><progress>10</progress><warnings/><details/></job></result></response>

#installed
#<response status="success"><result><job><tenq>2018/09/18 14:09:18</tenq><tdeq>14:09:18</tdeq><id>7713</id><admin>admin</admin><type>Antivirus</type><status>FIN</status><queued>NO</queued><stoppable>no</stoppable><result>OK</result><tfin>14:09:42</tfin><description/><positionInQ>0</positionInQ><progress>14:09:42</progress><details><line>Configuration committed successfully</line><line>Successfully committed last configuration</line></details><warnings/></job></result></response>

#Get and check job ID... Eventually add that logic

def upgrade_content(active_device, passive_device, api_key):
    '''
    Connects to both firewalls in a HA pair.  Downloads and
    Installs the 'latest' content definitions.
    Times out after 15 minutes.
    '''
    devices = (active_device, passive_device)
    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><content><upgrade><download><latest></latest></download></upgrade></content></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)

#Get and check job ID... Eventually add that logic
#/api/?type=op&cmd=<show><jobs><id></id></jobs></show>

    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><content><upgrade><install><version>latest</version></install></upgrade></content></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)

#Get and check job ID... Eventually add that logic

def upgrade_wildfire(active_device, passive_device, api_key):
    '''
    Connects to both firewalls in a HA pair.  Downloads and
    Installs the 'latest' wildfire definitions.
    Times out after 15 minutes.
    '''
    devices = (active_device, passive_device)
    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><wildfire><upgrade><download><latest></latest></download></upgrade></wildfire></request>&key={}'.format(device, api_key)
        dictionary_response = requests_response_to_dictionary(api_call)

    for device in devices:
        api_call = 'https://{}/api/?type=op&cmd=<request><wildfire><upgrade><install><version>latest</version></install></upgrade></wildfire></request>&key={}'.format(device, api_key)
        response = requests.get(api_call, verify=False)

#Get and check job ID... Eventually add that logic

#admin@FW2(active)> request wildfire upgrade download latest
#(container-tag: wildfire container-tag: upgrade container-tag: download container-tag: latest pop-tag: pop-tag: pop-tag: pop-tag:)
#((eol-matched: . #t) (context-inserted-at-end-p: . #f))


#<request cmd="op" cookie="9901621699572051" uid="500"><operations><request><wildfire><upgrade><download><latest/></downloa
#d></upgrade></wildfire></request></operations></request>

#2018-09-18 13:33:59
#<response status="error"><msg><line>No update available</line></msg></response>

#Server error : No update available

#Get and check job ID... Eventually add that logic

#def upgrade_url_filtering(active_device, passive_device, api_key):
#   Another day, another dollar
#   Requires logic to determine what or if URL filtering is being used

#
#<request><high-availability><state><suspend></suspend></state></high-availability></request>
#if
#<response status="success">
#<result>Successfully changed HA state to suspended</result>
#</response>
#else
#<response status="error">

#DEVICE WILL SUSPEND IF SECOND DEVICE IS DOWN.  Only will error on no ha or other issues

#scratch space

def check_firewall_license(device=None, api_key=None):
    '''
    Checks the current status of the active licenses.
    API call uses the IP address of the device and the api key
    '''
    api_call = 'https://{}/api/?type=op&cmd=<request><license><info></info></license></request>&key={}'.format(device, api_key)
    dictionary_response = requests_response_to_dictionary(api_call)
    json_response = json.dumps(dictionary_response, indent=4)
    print(json_response)
#    return json_response

def update_firewall_license(device=None, api_key=None, timeout=120):
    '''
    Updates, from the Internet, the device licensing.
    API call uses the IP address of the device and the api key
    '''
    api_call = 'https://{}/api/?type=op&cmd=<request><license><fetch></fetch></license></request>&key={}'.format(device, api_key)
    dictionary_response = requests_response_to_dictionary(api_call)
    json_response = json.dumps(dictionary_response, indent=4)
    print(json_response)
#    return json_response

def check_all_firewall_licenses():
    '''
    Looks at the config.py file for the tuple 'all_firewalls'
    Passes the IP Address and API Key into the check_firewall_license function
    Should probably do away with config.py file and move to a CLI?  IDK
    '''
    for device in config.all_firewalls:
        check_firewall_license(device['ip_address'], device['api_key'])

def update_all_firewall_licenses():
    '''
    Looks at the config.py file for the tuple 'all_firewalls'
    Passes the IP Address and API Key into the update_firewall_license function
    Should probably do away with config.py file and move to a CLI?  IDK
    '''
    for device in config.all_firewalls:
        update_firewall_license(device['ip_address'], device['api_key'])
