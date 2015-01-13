# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from firefoxtests.harness.testcase import FirefoxTestCase

homepage_pref = 'browser.startup.homepage'


class TestHomeButton(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.url = self.marionette.absolute_url('layout/mozilla.html')
        self.prefs.set_pref(homepage_pref, self.url)

    def tearDown(self):
        self.prefs.restore_pref(homepage_pref)
        FirefoxTestCase.tearDown(self)

    def test_home_button(self):
        self.browser.navbar.home_button.click()

        # TODO wait_for_page_load
        time.sleep(1)
        with self.marionette.using_context('content'):
            self.assertEquals(self.marionette.get_url(), self.url)
