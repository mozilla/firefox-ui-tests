# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase

class TestNewTab(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)
        url = '{}layout/mozilla.html'.format(self.marionette.baseurl)
        self.marionette.navigate(url)
        self.tabstrip = self.puppeteer.tabstrip
        self.toolbar = self.puppeteer.toolbar

    def tearDown(self):
        # TODO close active tab
        # bug 1088223: active_tab not working
        FirefoxTestCase.tearDown(self)

    def test_open_tab_by_newtab_button(self):
        self.marionette.set_context('chrome')

        num_tabs = len(self.tabstrip.tabs)
        self.tabstrip.newtab_button.click()
        self.assertEqual(len(self.tabstrip.tabs), num_tabs + 1)

        # TODO get this value from 'browser.newtab.url'
        self.assertEqual(self.toolbar.location, 'about:newtab')

