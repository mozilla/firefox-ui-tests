# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.decorators import skip_if_e10s
from firefox_ui_harness.testcase import FirefoxTestCase


class TestBrowserWindowShortcuts(FirefoxTestCase):

    # Test navigates between remote and non remote pages (bug 1096488)
    @skip_if_e10s
    def test_addons_manager(self):
        # If an about:xyz page is visible, no new tab will be opened
        with self.marionette.using_context('content'):
            self.marionette.navigate('about:')

        num_tabs = len(self.browser.tabbar.tabs)

        # TODO: To be moved to the upcoming add-ons library
        self.browser.send_shortcut(self.browser.get_localized_entity('addons.commandkey'),
                                   accel=True, shift=True)
        self.assertEqual(len(self.browser.tabbar.tabs), num_tabs + 1)

        # TODO: Marionette currently fails to detect the correct tab
        # with self.marionette.using_content('content'):
        #     self.wait_for_condition(lambda mn: mn.get_url() == "about:addons")

        self.marionette.close()

    def test_search_field(self):
        current_name = self.marionette.execute_script("""
            return window.document.activeElement.localName;
        """)

        # This doesn't test anything if we're already at input.
        self.assertNotEqual(current_name, "input")

        # TODO: To be moved to the upcoming search library
        if self.platform == 'linux':
            key = 'searchFocusUnix.commandkey'
        else:
            key = 'searchFocus.commandkey'
        self.browser.send_shortcut(self.browser.get_localized_entity(key),
                                   accel=True)

        # TODO: Check that the right input box is focused
        # Located below searchbar as class="autocomplete-textbox textbox-input"
        # Anon locator has not been released yet (bug 1080764)
        def has_input_selected(mn):
            selection_name = mn.execute_script("""
                return window.document.activeElement.localName;
            """)
            return selection_name == "input"

        self.wait_for_condition(has_input_selected)
