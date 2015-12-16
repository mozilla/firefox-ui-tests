#!/usr/bin/env python

"""Simplest version of the setup_development script from mozbase. We might want to switch
to the full version later. As of now the script has an infinite loop and doesn't process
anything.
"""

import subprocess
import sys

packages = [
    'firefox_ui_harness',
    'firefox_puppeteer',
    'firefox_ui_tests'
]

for package in packages:
    subprocess.check_call([sys.executable, 'setup.py', 'develop'],
                          cwd=package)
