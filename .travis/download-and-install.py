#!/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from mozdownload import FactoryScraper
import mozinstall


scraper = FactoryScraper('daily',
                         branch=os.environ['MOZ_BRANCH'],
                         locale=os.environ['LOCALE'])
installer_path = scraper.download()

install_path = mozinstall.install(installer_path, 'application')
binary_path = mozinstall.get_binary(install_path, 'firefox')

with open('binary.txt', 'w') as f:
    f.write(binary_path)
