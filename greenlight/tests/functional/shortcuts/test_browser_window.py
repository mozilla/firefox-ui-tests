# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.keys import Keys

from greenlight.harness.testcase import FirefoxTestCase


dtds = ['chrome://browser/locale/browser.dtd']


class TestBrowserWindowShortcuts(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.l10n = self.lib.l10n

    def test_addons_manager(self):
        self.marionette.set_context("chrome")

        key = self.l10n.get_localized_entity(dtds, 'addons.commandkey')

        # On Linux the shortcut will only work if no other text field has focus
        # TODO: Remove focus from the location bar

        # TODO: Sending keys globally to the browser window
        # Bug 1090925: Implement Action support for send_keys
        window = self.marionette.find_element('id', 'main-window')

        # CONTROL will only work on Linux and Windows. On OS X it is COMMAND.
        # TODO: We might want to request to get an ACCEL key added?
        window.send_keys(Keys.SHIFT + Keys.CONTROL + key)

        # TODO: wait for page being loaded?
        self.assertEqual(self.marionette.get_url(), 'about:addons')

    def test_search_field(self):
        self.marionette.set_context("chrome")

        if self.marionette.session_capabilities['platformName'] == 'LINUX':
            key = self.l10n.get_localized_entity(dtds,
                                                 'searchFocusUnix.commandkey')
        else:
            key = self.l10n.get_localized_entity(dtds,
                                                 'searchFocus.commandkey')

        # TODO: Sending keys globally to the browser window
        # Bug 1090925: Implement Action support for send_keys
        window = self.marionette.find_element('id', 'main-window')

        # CONTROL will only work on Linux and Windows. On OS X it is COMMAND.
        # TODO: We might want to request to get an ACCEL key added?
        window.send_keys(Keys.CONTROL + key)
        time.sleep(3)

        # TODO: Better way to retrieve this element?
        type = self.marionette.execute_script("""
            return window.document.activeElement.localName;
        """)

        # TODO: Check that the right input box is focused
        # Located below searchbar as class="autocomplete-textbox textbox-input"
        # Anon locator has not been released yet (bug 1080764)
        # searchbar = self.marionette.find_element('id', 'searchbar')
        self.assertEqual(type, 'input')
