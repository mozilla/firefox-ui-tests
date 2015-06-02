#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
The script can be used to setup a virtual environment for running Firefox UI Tests.
It will automatically install the firefox ui test package, all its dependencies,
and optional packages if specified.

"""

import optparse
import os
import shutil
import subprocess
import sys
import urllib2
import zipfile


# Link to the folder, which contains the zip archives of virtualenv
VIRTUALENV_URL = 'https://github.com/pypa/virtualenv/archive/%(VERSION)s.zip'
VIRTUALENV_VERSION = '12.1.1'

here = os.path.dirname(os.path.abspath(__file__))

venv_script_path = 'Scripts' if sys.platform == 'win32' else 'bin'
venv_activate = os.path.join(venv_script_path, 'activate')
venv_activate_this = os.path.join(venv_script_path, 'activate_this.py')
venv_python_bin = os.path.join(venv_script_path, 'python')

usage_message = """
***********************************************************************
To run the Firefox UI Tests, activate the virtual environment:
    {}{}

See firefox-ui-tests --help for all options

***********************************************************************
"""


def download(url, target):
    """Downloads the specified url to the given target."""
    response = urllib2.urlopen(url)
    with open(target, 'wb') as f:
        f.write(response.read())

    return target


def create_virtualenv(target, python_bin=None):
    script_path = os.path.join(here, 'virtualenv-%s' % VIRTUALENV_VERSION,
                               'virtualenv.py')

    print 'Downloading virtualenv %s' % VIRTUALENV_VERSION
    zip_path = download(VIRTUALENV_URL % {'VERSION': VIRTUALENV_VERSION},
                        os.path.join(here, 'virtualenv.zip'))

    try:
        with zipfile.ZipFile(zip_path, 'r') as f:
            f.extractall(here)

        print 'Creating new virtual environment'
        cmd_args = [sys.executable, script_path, target]

        if python_bin:
            cmd_args.extend(['-p', python_bin])

        subprocess.check_call(cmd_args)
    finally:
        try:
            os.remove(zip_path)
        except OSError:
            pass

        shutil.rmtree(os.path.dirname(script_path), ignore_errors=True)


def main():
    parser = optparse.OptionParser('Usage: %prog [options] path_to_venv')
    parser.add_option('-p', '--python',
                      type='string',
                      dest='python',
                      metavar='BINARY',
                      help='The Python interpreter to use.')
    parser.add_option('--with-optional-packages',
                      dest='with_optional',
                      default=False,
                      action='store_true',
                      help='Installs optional packages for enhanced usability.')
    (options, args) = parser.parse_args(args=None, values=None)

    if len(args) != 1:
        parser.error('Path to the environment has to be specified')
    target = args[0]
    assert target

    # Remove an already existent virtual environment
    if os.path.exists(target):
        print 'Removing already existent virtual environment at: %s' % target
        shutil.rmtree(target, True)

    create_virtualenv(target, python_bin=options.python)

    # Activate the environment
    tps_env = os.path.join(target, venv_activate_this)
    execfile(tps_env, dict(__file__=tps_env))

    # Install Firefox UI tests, dependencies and optional packages
    command = ['pip', 'install', os.getcwd()]
    if options.with_optional:
        command.extend(['-r', 'optional_packages.txt'])

    print 'Installing Firefox UI Tests and dependencies...'
    print 'Command: %s' % command
    subprocess.check_call(command)

    # Print the user instructions
    print usage_message.format('' if sys.platform == 'win32' else 'source ',
                               os.path.join(target, venv_activate))


if __name__ == "__main__":
    main()
