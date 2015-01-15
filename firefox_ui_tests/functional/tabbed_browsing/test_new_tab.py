# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase


class TestNewTab(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        with self.marionette.using_context('content'):
            url = self.marionette.absolute_url('layout/mozilla.html')
            self.marionette.navigate(url)

    def tearDown(self):
        self.marionette.close()
        FirefoxTestCase.tearDown(self)

    def test_open_tab_by_newtab_button(self):
        num_tabs = len(self.browser.tabbar.tabs)
        self.browser.tabbar.newtab_button.click()
        self.assertEqual(len(self.browser.tabbar.tabs), num_tabs + 1)

        newtab_url = self.prefs.get_pref('browser.newtab.url')
        self.assertEqual(self.browser.navbar.location, newtab_url)
