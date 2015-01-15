# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait
from marionette.errors import NoSuchElementException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestTabs(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        urls = [
            'layout/mozilla.html',
            'layout/mozilla_community.html',
            'layout/mozilla_contribute.html',
            'layout/mozilla_governance.html',
            'layout/mozilla_grants.html',
            'layout/mozilla_mission.html',
            'layout/mozilla_organizations.html',
            'layout/mozilla_projects.html',
        ]
        urls = [self.marionette.absolute_url(url) for url in urls]

        self.marionette.execute_script("""
            for (let i = 0; i < arguments.length; ++i) {
                gBrowser.addTab(arguments[i]);
            }
        """, script_args=urls)

        self.prefs.set_pref('browser.tabs.warnOnClose', False)
        self.prefs.set_pref('browser.tabs.warnOnCloseOtherTabs', False)

        def tabs_loaded(m):
            label = m.execute_script("""
              return gBrowser.tabs[gBrowser.tabs.length-1]
                             .getAttribute('label');
            """)
            return 'Projects' in label

        Wait(self.marionette).until(tabs_loaded)

    def tearDown(self):
        self.marionette.execute_script("""
            gBrowser.removeAllTabsBut(gBrowser.tabs[0]);
        """)

        self.wait_for_condition(lambda _: len(self.browser.tabbar.tabs) == 1)

        FirefoxTestCase.tearDown(self)

    def test_switch_to_tab(self):
        tabs = self.browser.tabbar.tabs

        self.browser.tabbar.switch_to_tab(3)
        self.assertEquals(self.browser.tabbar.active_tab, tabs[3])

        self.browser.tabbar.switch_to_tab('Mission')
        self.assertEquals(self.browser.tabbar.active_tab, tabs[6])

        self.browser.tabbar.switch_to_tab(tabs[4])
        self.assertEquals(self.browser.tabbar.active_tab, tabs[4])

    def test_close_tab(self):
        num_tabs = len(self.browser.tabbar.tabs)
        tab = self.browser.tabbar.get_tab('Mission')
        tab.close()

        self.assertEquals(len(self.browser.tabbar.tabs), num_tabs - 1)
        with self.assertRaises(NoSuchElementException):
            self.browser.tabbar.switch_to_tab('Mission')

    def test_newtab_button(self):
        num_tabs = len(self.browser.tabbar.tabs)
        self.browser.tabbar.newtab_button.click()
        self.assertEquals(len(self.browser.tabbar.tabs), num_tabs + 1)
