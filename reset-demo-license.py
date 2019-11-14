import utils
import keys_license
import time

devices = ['172.31.33.241']

creditials = utils.get_login_creditials()


def set_pa_portal_api_key():
    cmd = '<operations><request><license><api-key><set><key>' + keys_license.pa_portal_api_key + '</key></set></api-key></license></request></operations></request>'
    utils.xml_to_dictionary(utils.palo_alto_api_call(device, cmd, **creditials))


def deactive_license():
    cmd = '<request><license><deactivate><VM-Capacity><mode>auto</mode></VM-Capacity></deactivate></license></request>'
    utils.xml_to_dictionary(utils.palo_alto_api_call(device, cmd, **creditials))
    time.sleep(10)


def set_auth_key():
    '''
    This command reboots the device and returns garbage.
    '''
    cmd = '<request><license><fetch><auth-code>' + keys_license.auth_code + '</auth-code></fetch></license></request>'
    utils.palo_alto_api_call(device, cmd, **creditials)
    time.sleep(10)


for device in devices:
    set_pa_portal_api_key()
    deactive_license()
    utils.reboot()
    utils.wait_for_shutdown()
    utils.check_if_device_booted()
    set_auth_key()

# This works even tho API errors
# <request><license><fetch><auth-code>V3039712</auth-code></fetch></license></request>
