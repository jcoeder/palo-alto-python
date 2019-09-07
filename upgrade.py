#!/usr/bin/python3

import getpass
import requests
import xmltodict
import re
import datetime
import time
import difflib
import filecmp
from packaging.version import Version, parse, LegacyVersion
import utils

debug_to_console = True

'''
need to add wildfire check - /api/?type=op&cmd=<request><wildfire><upgrade><check></check></upgrade></wildfire></request>
need to add retrieve license from server
also need to add check and info request for each feature.


  <operations xml="yes">
    <request>
      <license>
        <info/>
      </license>
    </request>
  </operations>
</request>
[2019/07/09 21:32:11] user=5043298396328407
Response took 0.009s <response status="success"><result><licenses><entry><feature>GlobalProtect Portal</feature><description>GlobalProtect Portal License</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>Never</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>Threat Prevention</feature><description>Threat Prevention</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>April 23, 2017</expires><expired>yes</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>DNS Security</feature><description>Palo Alto Networks DNS Security License</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>PAN-DB URL Filtering</feature><description>Palo Alto Networks URL Filtering License</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>BrightCloud URL Filtering</feature><description>BrightCloud URL Filtering</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>PA-VM</feature><description>Standard VM-50 Eval</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 07, 2019</expires><expired>no</expired><authcode>V1688084</authcode></entry><entry><feature>WildFire License</feature><description>WildFire signature feed, integrated WildFire logs, WildFire API</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>GlobalProtect Gateway</feature><description>GlobalProtect Gateway License</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry><entry><feature>Premium</feature><description>24 x 7 phone support; advanced replacement hardware service</description><serial>015354000029994</serial><issued>July 09, 2019</issued><expires>September 09, 2019</expires><expired>no</expired><base-license-name>PA-VM</base-license-name><authcode></authcode></entry></licenses></result></response>
[2019/07/09 21:32:11] user=5043298396328407
<request cmd="get" obj="/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system" cookie="5043298396328407"/>
[2019/07/09 21:32:11] user=5043298396328407
Response took 0.033s <response status="success" code="19"><result total-count="1" count="1">
  <system>
    <type>
      <static/>
    </type>
    <update-server>updates.paloaltonetworks.com</update-server>
    <update-schedule>
      <threats>
        <recurring>
          <weekly>
            <day-of-week>wednesday</day-of-week>
            <at>01:02</at>
            <action>download-only</action>
          </weekly>
        </recurring>
      </threats>
    </update-schedule>
    <timezone>US/Pacific</timezone>
    <service>
      <disable-telnet>yes</disable-telnet>
      <disable-http>yes</disable-http>
    </service>
    <hostname>PA-VM</hostname>
    <server-verification>yes</server-verification>
    <dns-setting>
      <servers>
        <primary>172.31.51.51</primary>
        <secondary>172.31.51.52</secondary>
      </servers>
    </dns-setting>
    <ip-address>172.31.33.241</ip-address>
    <netmask>255.255.255.0</netmask>
    <default-gateway>172.31.33.1</default-gateway>
  </system>
</result></response>
[2019/07/09 21:32:12] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <show>
      <system>
        <setting>
          <url-database/>
        </setting>
      </system>
    </show>
  </operations>
</request>
[2019/07/09 21:32:12] user=5043298396328407
Response took 0.038s <response status="success"><result>paloaltonetworks</result></response>
[2019/07/09 21:32:13] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <content>
        <upgrade>
          <check/>
        </upgrade>
      </content>
    </request>
  </operations>
</request>
[2019/07/09 21:32:13] user=5043298396328407
Response took 1.075s <response status="success"><result><content-updates last-updated-at="2019/07/09 21:32:13 PDT"><entry><version>8162-5503</version><app-version>8162-5503</app-version><filename>panupv2-all-apps-8162-5503</filename><size>39</size><size-kb>40416</size-kb><released-on>2019/06/13 22:06:28 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8162-5503.html?__gda__=1563337933_511342c6c1144d53eabad994e3eea59c]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8163-5511</version><app-version>8163-5511</app-version><filename>panupv2-all-apps-8163-5511</filename><size>39</size><size-kb>40417</size-kb><released-on>2019/06/17 11:42:18 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8163-5511.html?__gda__=1563337933_b2848c2eb38bc7699b37c39acc499c70]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8169-5542</version><app-version>8169-5542</app-version><filename>panupv2-all-apps-8169-5542</filename><size>32</size><size-kb>33210</size-kb><released-on>2019/07/09 11:48:00 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8169-5542.html?__gda__=1563337933_9baa0ddae7af645e108aab284170a69c]]></release-notes><downloaded>yes</downloaded><current>yes</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8164-5515</version><app-version>8164-5515</app-version><filename>panupv2-all-apps-8164-5515</filename><size>32</size><size-kb>33075</size-kb><released-on>2019/06/18 23:07:29 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8164-5515.html?__gda__=1563337933_27de78436df8b5c5b6504102a5b8f145]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8161-5500</version><app-version>8161-5500</app-version><filename>panupv2-all-apps-8161-5500</filename><size>39</size><size-kb>40411</size-kb><released-on>2019/06/10 16:24:05 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8161-5500.html?__gda__=1563337933_c814c86a1a1734dd3bb6b36d35512982]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8166-5525</version><app-version>8166-5525</app-version><filename>panupv2-all-apps-8166-5525</filename><size>32</size><size-kb>33194</size-kb><released-on>2019/06/27 17:41:42 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8166-5525.html?__gda__=1563337933_3eebc3b8abb21810d24cf8497a234b48]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8168-5540</version><app-version>8168-5540</app-version><filename>panupv2-all-apps-8168-5540</filename><size>32</size><size-kb>33202</size-kb><released-on>2019/07/09 07:45:23 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8168-5540.html?__gda__=1563337933_ba6f27825871a99df9527da2428cb175]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry><entry><version>8165-5521</version><app-version>8165-5521</app-version><filename>panupv2-all-apps-8165-5521</filename><size>32</size><size-kb>33184</size-kb><released-on>2019/06/25 16:33:35 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/content/app-8165-5521.html?__gda__=1563337933_d539571a2f8caa026b2d5d094bf30f5d]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>Apps</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry>
</content-updates> </result></response>
[2019/07/09 21:32:14] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <wildfire>
        <upgrade>
          <check/>
        </upgrade>
      </wildfire>
    </request>
  </operations>
</request>
[2019/07/09 21:32:14] user=5043298396328407
Response took 1.031s <response status="success"><result><content-updates last-updated-at="2019/07/09 21:32:14 PDT"><entry><version>364977-367688</version><app-version>364977-367688</app-version><filename>panupv2-all-wildfire-364977-367688</filename><size>7</size><size-kb>7188</size-kb><released-on>2019/07/09 21:05:09 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/wildfire/WildfireExternal-v2-364977.html?__gda__=1563336324_6c13cf51604543c3264ac96bf6bd0b71]]></release-notes><downloaded>yes</downloaded><current>yes</current><previous>no</previous><installing>no</installing><features>wildfire</features><update-type>Full</update-type><feature-desc>PAN-OS 7.1 and later</feature-desc></entry><entry><version>364982-367693</version><app-version>364982-367693</app-version><filename>panupv2-all-wildfire-364982-367693</filename><size>7</size><size-kb>7188</size-kb><released-on>2019/07/09 21:30:17 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/wildfire/WildfireExternal-v2-364982.html?__gda__=1563337934_64e0cb6c547803528d4524de15b4a12e]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>wildfire</features><update-type>Full</update-type><feature-desc>PAN-OS 7.1 and later</feature-desc></entry>
</content-updates> </result></response>
[2019/07/09 21:32:14] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <wf-private>
        <upgrade>
          <check/>
        </upgrade>
      </wf-private>
    </request>
  </operations>
</request>
[2019/07/09 21:32:14] user=5043298396328407
Response took 0.005s <response status="success"><result><content-updates last-updated-at="never">
</content-updates> </result></response>
[2019/07/09 21:32:14] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <url-filtering>
        <info/>
      </url-filtering>
    </request>
  </operations>
</request>
[2019/07/09 21:32:14] user=5043298396328407
Response took 0.033s <response cmd="status" status="success"><result><url-filtering>
    <entry>
        <version>0</version>
        <current>yes</current>
        <previous>no</previous>
    </entry>
</url-filtering>
</result></response>
[2019/07/09 21:32:14] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <show>
      <system>
        <setting>
          <url-database/>
        </setting>
      </system>
    </show>
  </operations>
</request>
[2019/07/09 21:32:14] user=5043298396328407
Response took 0.039s <response status="success"><result>paloaltonetworks</result></response>
[2019/07/09 21:32:15] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <global-protect-clientless-vpn>
        <upgrade>
          <check/>
        </upgrade>
      </global-protect-clientless-vpn>
    </request>
  </operations>
</request>
[2019/07/09 21:32:15] user=5043298396328407
Response took 1.079s <response status="success"><result><content-updates last-updated-at="2019/07/09 21:32:15 PDT"><entry><version>78-161</version><app-version>78-161</app-version><filename>panup-all-gp-78-161</filename><size>0</size><size-kb>72</size-kb><released-on>2019/07/03 10:42:25 PDT</released-on><release-notes><![CDATA[https://downloads.paloaltonetworks.com/gpcontent/gpcontent-78-161.html?__gda__=1563337935_3238c92534cc5537fc3e965f2c54a9cf]]></release-notes><downloaded>no</downloaded><current>no</current><previous>no</previous><installing>no</installing><features>GlobalProtectClientlessVPN</features><update-type>Full</update-type><feature-desc>Unknown</feature-desc></entry>
</content-updates> </result></response>
[2019/07/09 21:32:15] user=5043298396328407
<request cmd="op" cookie="5043298396328407">
  <operations xml="yes">
    <request>
      <global-protect-gateway>
        <info/>
      </global-protect-gateway>
    </request>
  </operations>
</request>
[2019/07/09 21:32:15] user=5043298396328407
Response took 0.027s <response cmd="status" status="success"><result><global-protect-gateway>
    <entry>
        <version>unknown</version>
        <released-on>unknown</released-on>
        <current>no</current>
    </entry>
</global-protect-gateway>
</result></response>
[2019/07/09 21:32:15] user=5043298396328407
Call to [PanDirect.execute] /DynamicUpdates.check from router.php took 3.435s

'''


def debug_to_console(debug_to_console, item):
    '''
    Prints to screen only if debug_to_console is true.
    '''
    if debug_to_console is True:
        print(item)


def get_device():
    '''
    Ask user for IP address(es) of device.  Stores device(s) in a list
    '''
    device1 = str(input('IP Address of Primary device.\nPlease use OOB '
                        'management interfaces.\nIP Address: '))
    if device1 == '':
        device1 = None
    device2 = str(input('OPTIONAL: IP Address of Secondary device.\nPlease use '
                        'OOB management interfaces.\nIf device is a standalone '
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


def get_software_info():
    cmd = '/api/?type=op&cmd=<request><system><software><info></info></software></system></request>'
    software_info = xml_to_dictionary(
        palo_alto_api_call(device, cmd, **creditials)
        )
    return software_info


def delete_non_current_software():
    software_info = get_software_info()
    if software_info['response']['@status'] == 'error':
        pass
    else:
        for entry in software_info['response']['result']['sw-updates']['versions']['entry']:
            if entry['downloaded'] == 'yes' and entry['current'] == 'no':
                cmd = '/api/?type=op&cmd=<delete><software><version>' +\
                    entry['version'] + '</version></software></delete>'
                palo_alto_api_call(device, cmd, **creditials)


def fetch_licensing():
    '''
    Initiates the command that the devcies use to fetch their most up-to-date
    licensing information from the license server.
    '''
    cmd = '/api/?type=op&cmd=<request><license><fetch></fetch></license></request>'
    palo_alto_api_call(device, cmd, timeout=30, **creditials)


def get_licensing_infomation():
    '''
    '''
    cmd = '/api/?type=op&cmd=<request><license><info></info></license></request>'
    licensing_infomation = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    debug_to_console(debug_to_console, licensing_infomation)
    return licensing_infomation


def licensed_features():
    '''
    Places licensed features into a list.

    <response status="success">
      <result>
        <licenses>
            <entry>
                <feature>PA-VM</feature>
                <description>Standard VM-50 Eval</description>
                <serial>015354000025114</serial>
                <issued>March 02, 2019</issued>
                <expires>May 01, 2019</expires>
                <expired>no</expired>
                <authcode>V5321834</authcode>
            </entry>
            .......
            <entry>
                <feature>PAN-DB URL Filtering</feature>
                <description>Palo Alto Networks URL Filtering License</description>
                <serial>015354000025114</serial>
                <issued>March 02, 2019</issued>
                <expires>May 02, 2019</expires>
                <expired>no</expired>
                <base-license-name>PA-VM</base-license-name>
                <authcode></authcode>
            </entry>
          </licenses>
        </result>
    </response>

    becomes

    ['PA-VM', '.......', 'PAN-DB URL Filtering']

    Possible entries are:
    PA-VM
    PAN-DB URL Filtering
    Threat Prevention
    GlobalProtect Gateway
    WildFire License
    DNS Security
    BrightCloud URL Filtering
    GlobalProtect Portal
    Premium

    Unlicensed devices will not have entries.
    '''
    licensed_infomation = get_licensing_infomation()
    feature_list = []
    if licensed_infomation['response']['result']['licenses'] == None:
        feature_list = []
    else:
        for entry in licensed_infomation['response']['result']['licenses']['entry']:
            if entry['expired'] == 'no':
                feature_list.append(entry['feature'])
    print(feature_list)
    return feature_list


def xml_to_dictionary(xml):
    '''
    Fuction to convert an XML response into a dictionary
    and returns that as a dictionary.
    '''
    return xmltodict.parse(xml.text)


def get_serial_number(system_info):
    '''
    The system information contains the serial number.  This returns
    that serial number as a string.
    '''
    return system_info['response']['result']['system']['serial']


def xml_configuration_to_file(configuration, prefix):
    '''
    Uses the configuration either backup_running_config or
    backup_candidate_config and generates an identifiable name for the file
    then saves the file to the local directory.
    '''
    configuration_backup_file = open(prefix + '-' + serial_number + '-' + str(
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.xml', 'w')
    configuration_backup_file.write(configuration)
    file_name = configuration_backup_file.name
    return file_name


def get_ha_devices():
    '''
    Using ha_info the local-info and peer-info are checked for state.  This
    state is then stored in a dictionary.  Default to None as only active
    and passive OR active_primary and active_secondary will be used at any
    given time.  This allows this function to be used against active-passive
    or active-active HA pairs.
    '''
    active = None
    passive = None
    active_primary = None
    active_secondary = None

    peer1 = ha_info['response']['result']['group']['local-info']['mgmt-ip']
    if ha_info['response']['result']['group']['local-info']['state'] == 'active':
        active = re.sub(r'\/.*', '', peer1, count=1)

    elif ha_info['response']['result']['group']['local-info']['state'] == 'passive':
        passive = re.sub(r'\/.*', '', peer1, count=1)

    elif ha_info['response']['result']['group']['local-info']['state'] == 'active-primary':
        active_primary = re.sub(r'\/.*', '', peer1, count=1)

    elif ha_info['response']['result']['group']['local-info']['state'] == 'active-secondary':
        active_secondary = re.sub(r'\/.*', '', peer1, count=1)

    peer2 = ha_info['response']['result']['group']['peer-info']['mgmt-ip']
    if ha_info['response']['result']['group']['peer-info']['state'] == 'active':
        active = re.sub(r'\/.*', '', peer2, count=1)

    elif ha_info['response']['result']['group']['peer-info']['state'] == 'passive':
        passive = re.sub(r'\/.*', '', peer2, count=1)

    elif ha_info['response']['result']['group']['peer-info']['state'] == 'active-primary':
        active_primary = re.sub(r'\/.*', '', peer2, count=1)

    elif ha_info['response']['result']['group']['peer-info']['state'] == 'active-secondary':
        active_secondary = re.sub(r'\/.*', '', peer2, count=1)

    ha_devices = {
        'active': active,
        'passive': passive,
        'active_primary': active_primary,
        'active_secondary': active_secondary
        }

    return ha_devices


def disable_preemption():
    '''
    Disables HA preemption.  This is recommened to avoid unneed flapping during
    software upgrades and reboots.
    '''
    print('Disabling preemption.')
    cmd = "/api/?type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/deviceconfig/high-availability/group/entry[@name='1']&element=<election-option><preemptive>no</preemptive></election-option>"
    palo_alto_api_call(device, cmd, **creditials)
    commit(description='Disabling preemption.')


def enable_preemption():
    '''
    Enables HA preemption.
    '''
    print('Enabling preemption.')
    cmd = "/api/?type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/deviceconfig/high-availability/group/entry[@name='1']&element=<election-option><preemptive>yes</preemptive></election-option>"
    palo_alto_api_call(device, cmd, **creditials)
    commit(description='Enabling preemption.')


def pending_changes():
    '''
    Checks to see if there are pending changes.  Used by commit()
    to save time if no commit is needed.
    '''
    cmd = '/api/?type=op&cmd=<check><pending-changes></pending-changes></check>'
    pending_changes_dict = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    return pending_changes_dict


def commit(description=''):
    '''
    Check if there are pending changes.  If there are none, do not commit.
    This is just a time saver.  API will commit regardless.

    Commits candidate configuration to running configuration.  An option
    description can be added ot the commit if desired.

    Returns XML as follows:

    <response status="success" code="19">
      <result>
        <msg>
          <line>Commit job enqueued with jobid 4</line>
        </msg>
        <job>4</job>
      </result>
    </response>
    '''
    pending_changes_dict = pending_changes()

    if pending_changes_dict['response']['result'] == 'no':
        print('No changes to commit')
    else:
        print('Commiting configuration.')
        cmd = '/api/?type=commit&cmd=<commit><description>' + description + '</description></commit>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)


def backup_running_configuraiton():
    '''
    This function used backs up the XML of the running configuration file and
    saves it to the local directory with the format RUNNING-serial_number-date-time.xml
    Might use /api/?type=op&cmd=<show><config><running></running></config></show>
    instead of /api/?type=export&category=configuration
    '''
    print('Backing up the running configuration of device ' + device + ' with',\
          'serial number ' + serial_number + '.')
    cmd = '/api/?type=op&cmd=<show><config><running></running></config></show>'
    configuration = palo_alto_api_call(device, cmd, **creditials).text
    file_name = xml_configuration_to_file(configuration, 'RUNNING')
    print('Configuration backed up to ' + file_name)
    return file_name


def backup_candidate_configuration():
    '''
    This function used backs up the XML of the candidate configuration file and
    saves it to the local directory with the format CANDIDATE-serial_number-date-time.xml
    '''
    print('Backing up the candidate configuration of device ' + device + ' with',\
          'serial number ' + serial_number + '.')
    cmd = '/api/?type=op&cmd=<show><config><candidate></candidate></config></show>'
    configuration = palo_alto_api_call(device, cmd, **creditials).text
    file_name = xml_configuration_to_file(configuration, 'CANDIDATE')
    print('Configuration backed up to ' + file_name)
    return file_name


def all_upgrade_versions():
    '''
    Extract only the software versions which are upgrades from the current
    version and provide them as a list to the user.

    all_upgrade_versions is a list of strings ['8.1.6', '8.1.5', '8.1.4', '8.1.3', '8.1.2']
    '''
    all_available_versions_list = []
    all_upgrade_versions = []
    for versions in all_available_versions_dict['response']['result']['sw-updates']['versions']['entry']:
        all_available_versions_list.append(versions['version'])

    for entry in all_available_versions_list:
        if LegacyVersion(entry) > LegacyVersion(current_version_string):
            all_upgrade_versions.append(entry)
    return all_upgrade_versions


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


def get_system_info():
    '''
    Captures general system information.
    '''
    cmd = '/api/?type=op&cmd=<show><system><info></info></system></show>'
    system_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    return system_info


def get_ha_info():
    '''
    Returns ALL HA inforamtion about a device.
    '''
    cmd='/api/?type=op&cmd=<show><high-availability><all></all>\
         </high-availability></show>'
    return xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))


def check_ha_after_reboot():
    '''
    Only use against HA upgrade.  A rebooted HA device takes a while to start HA
    processes and will report HA as disabled until
    '''
    while True:
        time.sleep(3)
        ha_info = get_ha_info()
        if ha_info['response']['result']['enabled'] == 'no':
            continue
        elif ha_info['response']['result']['group']['local-info']['state'] == 'initial':
            continue
        elif ha_info['response']['result']['group']['local-info']['state'] == 'active' and ha_info['response']['result']['group']['peer-info']['state'] == 'passive':
            if ha_info['response']['result']['group']['local-info']['state-sync'] == 'Complete':
                print('HA State normal and state-sync is complete.')
                break
            else:
                continue
        elif ha_info['response']['result']['group']['local-info']['state'] == 'passive' and ha_info['response']['result']['group']['peer-info']['state'] == 'active':
            if ha_info['response']['result']['group']['local-info']['state-sync'] == 'Complete':
                print('HA State normal and state-sync is complete.')
                break
            else:
                continue
        elif ha_info['response']['result']['group']['local-info']['state'] == 'active-primary' and ha_info['response']['result']['group']['peer-info']['state'] == 'active-secondary':
            if ha_info['response']['result']['group']['local-info']['state-sync'] == 'Complete':
                print('HA State normal and state-sync is complete.')
                break
            else:
                continue
        elif ha_info['response']['result']['group']['local-info']['state'] == 'active-secondary' and ha_info['response']['result']['group']['peer-info']['state'] == 'active-primary':
            if ha_info['response']['result']['group']['local-info']['state-sync'] == 'Complete':
                print('HA State normal and state-sync is complete.')
                break
            else:
                continue
        else:
            continue


def rollback_uncommited_changes():
    print('Rolling back any uncommited changes.')
    cmd = '/api/?type=op&cmd=<load><config><last-saved></last-saved></config></load>'
    palo_alto_api_call(device, cmd, **creditials)


def get_current_version_string(system_info):
    '''
    Using system_info get the sw-version.  Return this version
    as a string.
    '''
    current_version_string = system_info['response']['result']['system']['sw-version']
    return current_version_string


def check_version_after_reboot():
    '''
    Gather system information and compare it against desired software
    version.  Should be used after device has rebooted.
    '''
    system_info_after_upgrade = get_system_info()
    version_after_upgrade = get_current_version_string(system_info_after_upgrade)
    if version_after_upgrade == desired_version:
        print('Successfully updated to ' + desired_version + '.')
    else:
        print('Software did NOT successfully update.')


def get_current_version_list():
    '''
    ['8', '0', '3']
    ['8', '0', '3-h4']
    '''
    current_version_list = current_version_string.split('.', 2)
    if '-' in current_version_list[2]:
        current_version_list[2] = current_version_list[2].split('-')[0]
    return current_version_list


def get_job_id(job_info):
    '''
    If a command returns a Job ID this function returns that ID
    as an interger.
    '''
    debug_to_console(debug_to_console, job_info)
    job_id = job_info['response']['result']['job']
    return job_id


def check_latest_software():
    '''
    Check for latest software.

    XML Formatted as follows:

    <response status="success">
    <result>
        <sw-updates last-updated-at="2019/04/12 17:16:27">
            <msg></msg>
            <versions>
                <entry>
                    <version>8.1.7</version>
                    <filename>PanOS_vm-8.1.7</filename>
                    <size>464</size>
                    <size-kb>475850</size-kb>
                    <released-on>2019/03/18  22:01:25</released-on>
                    <release-notes>
                        <![CDATA[https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os-release-notes]]>
                    </release-notes>
                    <downloaded>no</downloaded>
                    <current>no</current>
                    <latest>yes</latest>
                    <uploaded>no</uploaded>
                </entry>
                <entry>
                    <version>8.1.6</version>
                    <filename>PanOS_vm-8.1.6</filename>
                    <size>461</size>
                    <size-kb>473038</size-kb>
                    <released-on>2019/01/22  14:58:31</released-on>
                    <release-notes>
                        <![CDATA[https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os-release-notes]]>
                    </release-notes>
                    <downloaded>no</downloaded>
                    <current>no</current>
                    <latest>no</latest>
                    <uploaded>no</uploaded>
                </entry>
                ..........
                ..........
                <entry>
                    <version>6.1.0</version>
                    <filename>PanOS_vm-6.1.0</filename>
                    <size>364</size>
                    <size-kb>373149</size-kb>
                    <released-on>2014/10/25  09:29:59</released-on>
                    <release-notes>
                        <![CDATA[https://www.paloaltonetworks.com/documentation/61/pan-os/pan-os-release-notes]]>
                    </release-notes>
                    <downloaded>no</downloaded>
                    <current>no</current>
                    <latest>no</latest>
                    <uploaded>no</uploaded>
                </entry>
            </versions>
        </sw-updates>
    </result>
</response>

or it fails

<response status="error">
    <msg>
        <line>Failed to check upgrade info due to generic communication error. Please check network connectivity and try again.</line>
    </msg>
</response>
    '''
    cmd = '/api/?type=op&cmd=<request><system><software><check></check>\
        </software></system></request>'
    all_available_versions_dict = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    if all_available_versions_dict['response']['@status'] == 'error':
        print(all_available_versions_dict['response']['msg']['line'])
        if all_available_versions_dict['response']['msg']['line'] == 'Failed to check upgrade info due to generic communication error. Please check network connectivity and try again.':
            print('Please check licensing and management network connectivity.')
        exit()
    else:
        return all_available_versions_dict


def monitor_job_status(job_id):
    '''
    Monitor the status of the software download using the Job ID
    '''
    cmd = '/api/?type=op&cmd=<show><jobs><id>' + str(job_id) + '</id></jobs></show>'
    job_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    while True:
        time.sleep(1)
        job_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))

        # Display the job progress while it is under 99%
        if job_status['response']['result']['job']['status'] == 'ACT' and job_status['response']['result']['job']['result'] == 'PEND':
            if int(job_status['response']['result']['job']['progress']) <= 99:
                print('***** Job ' + job_status['response']['result']['job']['progress'] + '% Complete *****', end='\r', flush=True)

        # If a job finishes with a result okay.  Break out of loop.
        elif job_status['response']['result']['job']['status'] == 'FIN' and job_status['response']['result']['job']['result'] == 'OK':
            print('                                                        ', end='\r', flush=True)
            print('***** Job 100% Complete *****')
            break

        # If a job fails, print details and exit.
        elif job_status['response']['result']['job']['status'] == 'FIN' and job_status['response']['result']['job']['result'] == 'FAIL':
            print('                                                        ', end='\r', flush=True)
            print('***** Job FAILED *****')
            # Print error details
            print(job_status['response']['result']['job']['details'])
            exit()


def download_global_protect_client():
    '''
    Check for available Global Protect client versions.  Download the latest
    version.  DOES NOT INSTALL.  This should be manually installed when desired.
    '''
    if 'GlobalProtect Portal' and 'GlobalProtect Gateway' in feature_list:
        print('Downloading latest Global Protect client.')
        cmd = '/api/?type=op&cmd=<request><global-protect-client><software><check></check></software></global-protect-client></request>'
        check_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        if check_status['response']['@status'] == 'success':
            pass
        else:
            print('Checking for lastest Global Protect version failed.  Please check device Internet connection, licensing, and logs.')
            exit()
        cmd = '/api/?type=op&cmd=<request><global-protect-client><software><info></info></software></global-protect-client></request>'
        global_protect_versions = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        download_version = global_protect_versions['response']['result']['sw-updates']['versions']['entry'][0]['version']
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><global-protect-client><software><download><version>' + download_version + '</version></download></software></global-protect-client></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            cmd = '/api/?type=op&cmd=<request><global-protect-client><software><download><version>' + download_version + '</version><sync-to-peer>yes</sync-to-peer></download></software></global-protect-client></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)
        print('Downloaded latest Global Protect client.')
        print('Please manually install the client later.')


def delete_cached_content():
    '''
    Delete content filtering cache
    '''
    cmd = '/api/?type=op&cmd=<delete><content><cache><old-content></old-content></cache></content></delete>'
    palo_alto_api_call(device, cmd, **creditials)


def update_content_filtering():
    '''
    '''
    if 'PAN-DB URL Filtering' in feature_list:
        # Delete cached content filtering
        delete_cached_content()

        # Check for latest content filtering
        print('Updating latest content filtering database.')
        cmd = '/api/?type=op&cmd=<request><content><upgrade><check></check></upgrade></content></request>'
        check_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        if check_status['response']['@status'] == 'success':
            pass
        else:
            print('Checking for lastest content filtering database failed.  Please check device Internet connection, licensing, and logs.')
            exit()

        # Download latest content filtering
        print('Downloading latest content database.')
        # Standalone doesn't require sync-to-peer
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><content><upgrade><download><latest></latest></download></upgrade></content></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            # HA requires sync-to-peer
            if Version(current_version_string) < Version('8.0.5'):
                # Earlier versions expect sync-to-peer inside of latest
                cmd = '/api/?type=op&cmd=<request><content><upgrade><download><latest><sync-to-peer>yes</sync-to-peer></latest></download></upgrade></content></request>'
            else:
                # Later versions place sync-to-peer and latest inside download.
                cmd = '/api/?type=op&cmd=<request><content><upgrade><download><sync-to-peer>yes</sync-to-peer><latest></latest></download></upgrade></content></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)

        # Install latest content filtering
        print('Installing latest content database.')
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><content><upgrade><install><version>latest</version></install></upgrade></content></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            cmd = '/api/?type=op&cmd=<request><content><upgrade><install><version>latest</version><sync-to-peer>yes</sync-to-peer></install></upgrade></content></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)
        print('Latest content database installed.')


def update_wildfire():
    '''
    '''
    if 'WildFire License' in feature_list:
        print('Updating Wildfire database.')
        cmd = '/api/?type=op&cmd=<request><wildfire><upgrade><check></check></upgrade></wildfire></request>'
        check_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        if check_status['response']['@status'] == 'success':
            pass
        elif check_status['response']['@status'] == 'error' and check_status['response']['msg']['line'] == 'No update available':
            print('No Wildfire updates available.')
            return None
        else:
            print('Checking for lastest Wildfire failed.  Please check device Internet connection, licensing, and logs.')
            exit()

        print('Downloading latest Wildfire database.')
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><wildfire><upgrade><download><latest></latest></download></upgrade></wildfire></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            cmd = '/api/?type=op&cmd=<request><wildfire><upgrade><download><latest><sync-to-peer>yes</sync-to-peer></latest></download></upgrade></wildfire></request>'
        response = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        if response['response']['@status'] == 'error' and response['response']['msg']['line'] == 'No update available':
            print('No Wildfire updates available.')
            return None
        else:
            pass
        job_info = response
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)

        print('Installing latest Wildfire database.')
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><wildfire><upgrade><install><version>latest</version></install></upgrade></wildfire></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            cmd = '/api/?type=op&cmd=<request><wildfire><upgrade><install><version>latest</version><sync-to-peer>yes</sync-to-peer></install></upgrade></wildfire></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)
        print('Latest Wildfire database installed.')


def update_anti_virus():
    '''
    Threat Prevention
    '''
    if 'Threat Prevention' in feature_list:
        print('Updating anti-virus definitions.')
        cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><check></check></upgrade></anti-virus></request>'
        check_status = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        if check_status['response']['@status'] == 'success':
            pass
        else:
            print('Checking for lastest anti-virus definitions failed.  Please check device Internet connection, licensing, and logs.')
            exit()
        print('Downloading latest anti-virus definitions.')
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><download><latest></latest></download></upgrade></anti-virus></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            if Version(current_version_string) < Version('8.0.5'):
                # Earlier versions expect sync-to-peer inside of latest
                cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><download><latest><sync-to-peer>yes</sync-to-peer></latest></download></upgrade></anti-virus></request>'
            else:
                # Later versions place sync-to-peer and latest inside download.
                cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><download><sync-to-peer>yes</sync-to-peer><latest></latest></download></upgrade></anti-virus></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)
        print('Installing latest anti-virus definitions.')
        if ha_info['response']['result']['enabled'] == 'no':
            cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><install><version>latest</version></install></upgrade></anti-virus></request>'
        elif ha_info['response']['result']['enabled'] == 'yes':
            cmd = '/api/?type=op&cmd=<request><anti-virus><upgrade><install><version>latest</version><sync-to-peer>yes</sync-to-peer></install></upgrade></anti-virus></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        job_id = get_job_id(job_info)
        monitor_job_status(job_id)
        print('Latest anti-virus definitions installed.')


def diff_candidate_running_config(candidate_configuration, running_configuration):
    '''
    Compare the running vs the candidate configuration and ask the user to continue.
    '''
    candidate_configuration_text = open(candidate_configuration).readlines()
    running_configuration_text = open(running_configuration).readlines()

    if filecmp.cmp(candidate_configuration, running_configuration) is True:
        print('There are no pending changes.')
        return None

    for line in difflib.unified_diff(candidate_configuration_text, running_configuration_text):
        print(line,)

    print('These changes will be lost.  Would you like to continue?')
    print('')
    while True:
        response = input('Y or N : ')
        response = response.upper()
        if response == 'Y':
            break
        elif response == 'YES':
            break
        elif response == 'N':
            print('Exiting.')
            exit()
        elif response == 'NO':
            print('Exiting.')
            exit()


def get_desired_version():
    '''
    Ask the user which version they wish to upgrade to.  Will only return
    if the user provides a version in the list of all_upgrade_versions.
    '''
    # Set to None to prompt user.  Set to specific version for testing.
    # Example '8.1.7'
    desired_version = None
    if desired_version == None:
        while True:
            desired_version = str(input('Please select version to download: '))
            if desired_version in all_upgrade_versions:
                return desired_version
            else:
                print('')
                print('Please select available version from list provided.')
                print(all_upgrade_versions)
    return desired_version


def get_major_minor_base_release():
    '''
    If current version is 8.1.9 and desired version is 9.0.3.  9.0.0 must also
    be downloaded but does not have to be installed.
    '''
    if Version(desired_version).release[0] > Version(current_version_string).release[0]:
        base_version = str(Version(desired_version).release[0]) + '.0' + '.0'
        print('Downloading base version ' + base_version + '.')
        return base_version
    elif (Version(desired_version).release[0] == Version(current_version_string).release[0]) and (Version(desired_version).release[1] > Version(current_version_string).release[1]):
        base_version = str(Version(desired_version).release[0]) + '.' + str(Version(desired_version).release[1]) + '.0'
        print('Downloading base version ' + base_version + '.')
        return base_version
    elif (Version(desired_version).release[0] == Version(current_version_string).release[0]) and (Version(desired_version).release[1] == Version(current_version_string).release[1]):
        return None


def download_base_software():
    '''
    '''
    # Start the download of the software and capture the Job ID
    base_version = get_major_minor_base_release()
    if base_version != None:
        cmd = '/api/?type=op&cmd=<request><system><software><download><version>' +\
            base_version + '</version><sync-to-peer>yes</sync-to-peer></download></software></system></request>'
        job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
        monitor_job_status(get_job_id(job_info))
    else:
        pass


def download_software():
    '''
    '''
    # Start the download of the software and capture the Job ID
    monitor_job_status(get_job_id(job_info))
    print('Downloading version ' + desired_version + '.')
    if ha_info['response']['result']['enabled'] == 'no':
        cmd = '/api/?type=op&cmd=<request><system><software><download><version>' +\
            desired_version + '</version></download></software></system></request>'
    elif ha_info['response']['result']['enabled'] == 'yes':
        cmd = '/api/?type=op&cmd=<request><system><software><download><version>' +\
            desired_version + '</version><sync-to-peer>yes</sync-to-peer></download></software></system></request>'
    job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    monitor_job_status(get_job_id(job_info))


def install_software():
    '''
    '''
    # Install the downloaded software
    print('Installing version ' + desired_version + '.')
    cmd = '/api/?type=op&cmd=<request><system><software><install><version>' +\
        desired_version + '</version></install></software></system></request>'
    job_info = xml_to_dictionary(palo_alto_api_call(device, cmd, **creditials))
    monitor_job_status(get_job_id(job_info))


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


# Disable SSL Warnings
requests.urllib3.disable_warnings()

# Pull first device in list
device = get_device()[0]

# Store login information
creditials = utils.get_login_creditials()

# Retrieve HA Information and format it into a dictionary
ha_info = get_ha_info()


# Determine what HA mode is running
if ha_info['response']['result']['enabled'] == 'no':
    print('Performing standalone software upgrade.')

    # Get System Information
    system_info = get_system_info()

    # Get current version
    current_version_string = get_current_version_string(system_info)

    # Capture licensed features
    feature_list = licensed_features()

    # Get Serial Number from System Information
    serial_number = get_serial_number(system_info)

    # Backup the configuration and save it to the local directory
    candidate_configuration_file_name = backup_candidate_configuration()

    # Backup the running configuration and save it to the local directory
    running_configuration_file_name = backup_running_configuraiton()

    diff_candidate_running_config(candidate_configuration_file_name, running_configuration_file_name)

    # Rollback any unsaved configuration changes
    rollback_uncommited_changes()

    delete_non_current_software()

    # Check for Global Protect updates
    download_global_protect_client()

    # Update content filtering database
    update_content_filtering()

    # Update Wildfire database
    update_wildfire()

    # Update anti-virus definitions
    update_anti_virus()

    # Check current software version
    current_version_list = get_current_version_list()

    # Check for latest software
    all_available_versions_dict = check_latest_software()

    # Get all software versions that are upgrades from the current version
    all_upgrade_versions = all_upgrade_versions()
    print('Current versions is : ' + current_version_string + '.')
    print(all_upgrade_versions)

    # Ask user which version to upgrade to
    desired_version = get_desired_version()

    # Download and install software
    download_base_software()
    download_software()
    install_software()

    # Reboot the device
    reboot()

    # Wait for device to shutdown services before starting
    # full system checks
    wait_for_shutdown()

    # Check if device is up.
    check_if_device_booted()

    # Check to see if we upgraded to desired version
    check_version_after_reboot()

elif ha_info['response']['result']['enabled'] == 'yes' and ha_info['response']['result']['group']['mode'] == 'Active-Passive':
    ha_mode = 'active-passive'
    print('Performing an active-passive software upgrade.')

    # Get System Information
    system_info = get_system_info()

    # Get current version
    current_version_string = get_current_version_string(system_info)

    # Capture licensed features
    feature_list = licensed_features()

    # Get information about the HA Pair
    ha_devices = get_ha_devices()
    active = ha_devices['active']
    passive = ha_devices['passive']
    ha_pair = [active, passive]

    for device in ha_pair:
        device_system_info = get_system_info()

        # Get Serial Number from System Information
        serial_number = get_serial_number(device_system_info)

        # Backup the configuration and save it to the local directory
        candidate_configuration_file_name = backup_candidate_configuration()

        # Backup the running configuration and save it to the local directory
        running_configuration_file_name = backup_running_configuraiton()

        diff_candidate_running_config(candidate_configuration_file_name, running_configuration_file_name)

        # Rollback any unsaved configuration changes
        rollback_uncommited_changes()

    for device in ha_pair:
        # Delete unused software versions
        delete_non_current_software()

    for device in ha_pair:
        # Disable preemption
        disable_preemption()

    # Check for Global Protect updates
    download_global_protect_client()

    # Update content filtering database
    update_content_filtering()

    # Update Wildfire database
    update_wildfire()

    # Update and Install anti-virus
    update_anti_virus()

    # Check current software version
    current_version_list = get_current_version_list()

    # Check for latest software
    all_available_versions_dict = check_latest_software()

    # Get all software versions that are upgrades from the current version
    all_upgrade_versions = all_upgrade_versions()
    print('Current versions is : ' + current_version_string + '.')
    print(all_upgrade_versions)

    # Ask user which version to upgrade to
    desired_version = get_desired_version()

    # Download software to both devices
    download_base_software()
    download_software()

    # Change context to passive device
    device = passive

    # Install software to secondary device
    install_software()

    # Reboot secondary device
    reboot()

    # Wait for device to shutdown services before starting
    # full system checks
    wait_for_shutdown()

    # Check if device is up
    check_if_device_booted()

    # Check to see if upgraded to desired version
    check_version_after_reboot()

    # Wait for HA status to return to normal
    check_ha_after_reboot()

    # Change context to active device
    device = active

    # Install software on primary device
    install_software()

    # Reboot primary device
    reboot()

    # Wait for device to shutdown services before starting
    # full system checks
    wait_for_shutdown()

    # Check if device is up.
    check_if_device_booted()

    # Check to see if we upgraded to desired version
    check_version_after_reboot()

    # Wait for HA status to return to normal.
    check_ha_after_reboot()

    for device in ha_pair:
        # Reenable HA Preemtpion
        enable_preemption()

elif ha_info['response']['result']['enabled'] == 'yes' and ha_info['response']['result']['group']['mode'] == 'Active-Active':
    ha_mode = 'active-active'
    print('Performing an active-active software upgrade.')

    # Get System Information
    system_info = get_system_info()

    # Get current version
    current_version_string = get_current_version_string(system_info)

    # Capture licensed features
    feature_list = licensed_features()

    # Get information about the HA Pair
    ha_devices = get_ha_devices()
    active_primary = ha_devices['active_primary']
    active_secondary = ha_devices['active_secondary']
    ha_pair = [active_primary, active_secondary]

    for device in ha_pair:
        device_system_info = get_system_info()

        # Get Serial Number from System Information
        serial_number = get_serial_number(device_system_info)

        # Backup the configuration and save it to the local directory
        candidate_configuration_file_name = backup_candidate_configuration()

        # Backup the running configuration and save it to the local directory
        running_configuration_file_name = backup_running_configuraiton()

        diff_candidate_running_config(candidate_configuration_file_name, running_configuration_file_name)

        # Rollback any unsaved configuration changes
        rollback_uncommited_changes()

    for device in ha_pair:
        # Delete unused software versions
        delete_non_current_software()

    for device in ha_pair:
        # Disable preemption
        disable_preemption()

    # Check for Global Protect updates
    download_global_protect_client()

    # Update content filtering database
    update_content_filtering()

    # Update Wildfire database
    update_wildfire()

    # Update anti-virus definitions
    update_anti_virus()

    # Check current software version
    current_version_list = get_current_version_list()

    # Check for latest software
    all_available_versions_dict = check_latest_software()

    # Get all software versions that are upgrades from the current version
    all_upgrade_versions = all_upgrade_versions()
    print('Current versions is : ' + current_version_string + '.')
    print(all_upgrade_versions)

    # Ask user which version to upgrade to
    desired_version = get_desired_version()

    # Download software to both devices
    download_base_software()
    download_software()

    # Change context to secondary device
    device = active_secondary

    # Install software on secondary device
    install_software()

    # Reboot secondary device
    reboot()

    # Wait for device to shutdown services before starting
    # full system checks
    wait_for_shutdown()

    # Check if device is up.
    check_if_device_booted()

    # Check to see if we upgraded to desired version
    check_version_after_reboot()

    # Wait for HA status to return to normal.
    check_ha_after_reboot()

    # Change context to primary device
    device = active_primary

    # Install software on primary device
    install_software()

    # Reboot primary device
    reboot()

    # Wait for device to shutdown services before starting
    # full system checks
    wait_for_shutdown()

    # Check if device is up.
    check_if_device_booted()

    # Check to see if we upgraded to desired version
    check_version_after_reboot()

    # Wait for HA status to return to normal.
    check_ha_after_reboot()

    for device in ha_pair:
        # Renable HA Preemtion
        enable_preemption()

else:
    print('HA is not properly configured.')
    exit()
