# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.decorators import uses_lib
from greenlight.harness.testcase import FirefoxTestCase


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

        self.marionette.set_context('chrome')
        self.marionette.execute_script("""
            for (let i = 0; i < arguments.length; ++i) {
                gBrowser.addTab(arguments[i]);
            }
        """, script_args=urls)

        self.lib.prefs.set_pref('browser.tabs.warnOnClose', False)
        self.lib.prefs.set_pref('browser.tabs.warnOnCloseOtherTabs', False)

    def tearDown(self):
        self.marionette.execute_script("""
            gBrowser.removeAllTabsBut(gBrowser.tabs[0]);
        """)
        self.lib.prefs.restore_pref('browser.tabs.warnOnClose')
        self.lib.prefs.restore_pref('browser.tabs.warnOnCloseOtherTabs')
        
        FirefoxTestCase.tearDown(self)
            
    @uses_lib('tabstrip')
    def test_switch_to_tab(self):
        tabs = self.tabstrip.tabs

        self.tabstrip.switch_to_tab(3)
        self.assertEquals(self.tabstrip.active_tab, tabs[3])

        self.tabstrip.switch_to_tab('Mission')
        self.assertEquals(self.tabstrip.active_tab, tabs[6])

        self.tabstrip.switch_to_tab(tabs[4])
        self.assertEquals(self.tabstrip.active_tab, tabs[4])

    @uses_lib('tabstrip')
    def test_newtab_button(self):
        num_tabs = len(self.tabstrip.tabs)
        self.tabstrip.newtab_button.click()
        self.assertEquals(len(self.tabstrip.tabs), num_tabs + 1)
