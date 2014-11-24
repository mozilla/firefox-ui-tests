# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import NoSuchElementException

from greenlight.harness.decorators import uses_lib
from greenlight.harness.testcase import FirefoxTestCase


class TestBrowser(FirefoxTestCase):

    def test_window_element(self):
        first_window = self.browser.current_window
        self.assertEquals(first_window.tag_name, 'window')
        self.assertEquals(first_window.get_attribute('id'), 'main-window')

        self.assertEquals(len(self.browser.windows), 1)
        self.assertEquals(len(self.marionette.window_handles), 1)
        first_window.send_shortcut('ctrl-n')

        self.assertEquals(len(self.browser.windows), 2)
        self.assertEquals(len(self.marionette.window_handles), 2)
        for handle in self.marionette.window_handles:
            if handle != first_window.handle:
                self.marionette.switch_to_window(handle)
                break

        second_window = self.browser.current_window
        self.assertNotEquals(first_window.handle, second_window.handle)

        first_window.switch_to()
        self.assertEquals(first_window.handle, self.marionette.current_window_handle)
        second_window.close()
        self.assertEquals(first_window.handle, self.marionette.current_window_handle)
        self.assertEquals(len(self.marionette.window_handles), 1)

    def test_switch_to_window(self):
        url = self.marionette.absolute_url('layout/mozilla')

        first_window = self.browser.current_window
        first_window.send_shortcut('ctrl-n')
        first_window.send_shortcut('ctrl-n')

        windows = self.browser.windows
        self.assertEquals(len(windows), 3)

        with self.marionette.using_context('content'):
            self.marionette.navigate(url)

        self.browser.switch_to_window(windows[1])
        self.assertEquals(windows[1].handle, self.marionette.current_window_handle)

        self.browser.switch_to_window(windows[2].handle)
        self.assertEquals(windows[2].handle, self.marionette.current_window_handle)

        def is_my_window():
            with self.marionette.using_context('content'):
                return self.marionette.get_url() == url

        self.browser.switch_to_window(is_my_window)
        self.assertEquals(windows[0].handle, self.marionette.current_window_handle)

        with self.assertRaises(NoSuchElementException):
            self.browser.switch_to_window("humbug")

        with self.assertRaises(NoSuchElementException):
            self.browser.switch_to_window(lambda: False)

        windows[1].close()
        windows[2].close()
