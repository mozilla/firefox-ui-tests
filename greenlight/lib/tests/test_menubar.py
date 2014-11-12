# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import NoSuchElementException

from greenlight.harness.decorators import uses_lib
from greenlight.harness.testcase import FirefoxTestCase


class TestMenuBar(FirefoxTestCase):

    @uses_lib('menubar', 'tabstrip')
    def test_click_item_in_menubar(self):
        num_tabs = len(self.tabstrip.tabs)
        self.menubar.select('File', 'New Tab')
        self.assertEquals(len(self.tabstrip.tabs), num_tabs + 1)

    @uses_lib('menubar')
    def test_click_non_existent_menu_and_item(self):
        with self.assertRaises(NoSuchElementException):
            self.menubar.select('Foobar', 'New Tab')
        
        with self.assertRaises(NoSuchElementException):
            self.menubar.select('File', 'Foobar')
