# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys

from greenlight.harness.testcase import FirefoxTestCase
from greenlight.harness.decorators import uses_lib
from marionette import errors

class TestAboutPrivateBrowsing(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.pb_url = self.marionette.absolute_url('private_browsing/about.html?')
        self.dtds = ["chrome://branding/locale/brand.dtd",
                     "chrome://browser/locale/browser.dtd",
                     "chrome://browser/locale/aboutPrivateBrowsing.dtd"]

    def tearDown(self):
        self.marionette.close()

    def testCheckAboutPrivateBrowsing(self):
        self.prefs.set_pref('app.support.baseURL', self.pb_url)

        self.marionette.set_context('content')
        self.marionette.navigate('about:privatebrowsing')

        description = self.l10n.get_localized_entity(self.dtds,
                                                     'aboutPrivateBrowsing.subtitle.normal')

        self.marionette.set_context('content')
        status_node = self.marionette.find_element('css selector', 'p.showNormal')
        self.assertEqual(description, status_node.text,
                         "Status text indicates we are in private browsing mode")

        access_key = self.l10n.get_localized_entity(self.dtds,
                                                    'privatebrowsingpage.openPrivateWindow.accesskey')
        base_window = self.marionette.current_window_handle
        self.marionette.set_context('content')
        # Send keys to the top html element.
        top_html = self.marionette.find_element('tag name', 'html')
        top_html.send_keys(self.keys.SHIFT, self.keys.ACCEL, access_key)


        self.wait_for_condition(lambda mn: len(mn.window_handles) == 2)
        windows = self.marionette.window_handles
        windows.remove(base_window)
        pvt_win = windows[0]
        self.marionette.switch_to_window(pvt_win)

        def find_element(mn):
            try:
                link = self.marionette.find_element('id', 'learnMore')
                link.click()
                return True
            except errors.NoSuchElementException:
                return False
        self.wait_for_condition(find_element)

        self.marionette.set_context('chrome')
        self.assertEqual(2, len(self.tabstrip.tabs),
                         "A new tab has been opened")

        target_url = self.pb_url + 'private-browsing'
        url_bar = self.marionette.find_element('id', 'urlbar')

        # TODO: get_url does not correspond to what we want here.
        self.assertIn(url_bar.get_attribute('value'), target_url)

        self.prefs.restore_pref('app.support.baseURL')
