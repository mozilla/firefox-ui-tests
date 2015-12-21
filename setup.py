# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

PACKAGE_VERSION = '0.3'

deps = [
    'marionette-client == 2.0.0',
    'marionette-driver == 1.1.1',
    'mozfile == 1.2',
    'mozinfo == 0.8',
    'mozinstall == 1.12',
    'mozlog == 3.0',
]

setup(name='firefox-ui-tests',
      version=PACKAGE_VERSION,
      description='A collection of Mozilla Firefox UI tests run with Marionette',
      long_description='See https://github.com/mozilla/firefox-ui-tests',
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='mozilla',
      author='Mozilla Automation and Tools Team',
      author_email='tools@lists.mozilla.org',
      url='https://github.com/mozilla/firefox-ui-tests',
      license='MPL 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
        [console_scripts]
        firefox-ui-tests = firefox_ui_harness:cli
        firefox-ui-functional = firefox_ui_harness.cli_functional:cli_functional
        firefox-ui-update = firefox_ui_harness.cli_update:cli_update
      """)
