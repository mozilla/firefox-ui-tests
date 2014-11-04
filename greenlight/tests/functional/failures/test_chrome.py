# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from greenlight.harness.testcase import FirefoxTestCase


class TestChromeScope(FirefoxTestCase):

    def test_navigate_url(self):
        self.marionette.set_context('chrome')

        test_url = self.marionette.absolute_url('layout/mozilla.html')
        self.marionette.navigate(test_url)
        self.assertEquals(self.marionette.get_url(), test_url)
