# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness import FirefoxTestCase


@unittest.skip('Bug 1121710 - Fix MenuBar class for correct handling of menus')
class TestMenuBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

    def test_click_item_in_menubar(self):
        num_tabs = len(self.browser.tabbar.tabs)

        def opener(_):
            # Hard-coded labels will not work in localized builds
            self.browser.menubar.select('File', 'New Tab')

        self.browser.tabbar.open_tab(trigger=opener)

        self.browser.tabbar.tabs[-1].close()

    def test_click_non_existent_menu_and_item(self):
        with self.assertRaises(NoSuchElementException):
            # Hard-coded labels will not work in localized builds
            self.browser.menubar.select('Foobar', 'New Tab')

        with self.assertRaises(NoSuchElementException):
            # Hard-coded labels will not work in localized builds
            self.browser.menubar.select('File', 'Foobar')
