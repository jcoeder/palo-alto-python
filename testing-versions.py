from packaging.version import Version, parse, Version
desired_version = '9.0.3-h4'
current_version_string = '8.1.0'


def get_major_minor_base_release():
    '''
    If current version is 8.1.9 and desired version is 9.0.3.  9.0.0 must also
    be downloaded but does not have to be installed.
    '''
    desired_version_strip = desired_version.split('-')[0]

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


get_major_minor_base_release()
