# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase
from greenlight.harness.decorators import uses_lib

dtds = ['chrome://browser/locale/browser.dtd']


class TestBrowserWindowShortcuts(FirefoxTestCase):

    def setUp(self):
        super(TestBrowserWindowShortcuts, self).setUp()
        self.main_window = self.marionette.find_element("id", "main-window")

    def test_addons_manager(self):
        key = self.l10n.get_localized_entity(dtds, 'addons.commandkey')

        # On Linux the shortcut will only work if no other text field has focus
        # TODO: Remove focus from the location bar
        self.main_window.send_keys(self.keys.SHIFT, self.keys.ACCEL, key)
        self.marionette.set_context("content")
        self.wait_for_condition(lambda mn: mn.get_url() == "about:addons")

    def test_search_field(self):
        current_name = self.marionette.execute_script("return window.document.activeElement.localName;");
        # This doesn't test anything if we're already at input.
        self.assertNotEqual(current_name, "input")

        keys = [self.keys.ACCEL]
        if self.marionette.session_capabilities['platformName'] == 'LINUX':
            keys.append(self.l10n.get_localized_entity(dtds,
                                                       'searchFocusUnix.commandkey'))
        else:
            keys.append(self.l10n.get_localized_entity(dtds,
                                                       'searchFocus.commandkey'))

        # CONTROL will only work on Linux and Windows. On OS X it is COMMAND.
        self.main_window.send_keys(*keys)

        # TODO: Check that the right input box is focused
        # Located below searchbar as class="autocomplete-textbox textbox-input"
        # Anon locator has not been released yet (bug 1080764)
        def has_input_selected(mn):
            selection_name = mn.execute_script("return window.document.activeElement.localName;");
            return selection_name == "input"

        self.wait_for_condition(has_input_selected)
