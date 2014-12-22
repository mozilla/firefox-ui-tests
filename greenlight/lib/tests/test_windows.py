# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By
from marionette.errors import NoSuchElementException

from greenlight.harness.testcase import FirefoxTestCase


class TestWindows(FirefoxTestCase):

    def test_switch_to_window(self):
        url = self.marionette.absolute_url('layout/mozilla')

        first_window = self.windows.current

        # Those actions will fail if the current window is not a browser window
        first_window.send_shortcut('ctrl-n')
        first_window.send_shortcut('ctrl-n')

        windows = self.windows.all
        self.assertEquals(len(windows), 3)

        with self.marionette.using_context('content'):
            self.marionette.navigate(url)

        self.windows.switch_to(windows[1])
        self.assertEquals(windows[1].handle,
                          self.marionette.chrome_window_handle)

        self.windows.switch_to(windows[2].handle)
        self.assertEquals(windows[2].handle,
                          self.marionette.chrome_window_handle)

        def is_my_window(win):
            with self.marionette.using_context('content'):
                return self.marionette.get_url() == url

        self.windows.switch_to(is_my_window)
        self.assertEquals(windows[0].handle,
                          self.marionette.chrome_window_handle)

        with self.assertRaises(NoSuchElementException):
            self.windows.switch_to("humbug")

        with self.assertRaises(NoSuchElementException):
            self.windows.switch_to(lambda win: False)

        windows[1].close()
        windows[2].close()

    def test_base_window(self):
        self.assertEquals(len(self.windows.all), 1)
        self.assertEquals(len(self.marionette.chrome_window_handles), 1)

        first_window = self.windows.current
        self.assertEquals(first_window.handle,
                          self.marionette.chrome_window_handle)
        self.assertEquals(first_window.get_attribute('windowtype'),
                          self.marionette.get_window_type())
        self.assertEquals(first_window.window,
                          self.marionette.find_element(By.CSS_SELECTOR,
                                                       ':root'))

        # This action will fail if the current window is not a browser window
        first_window.send_shortcut('ctrl-n')

        self.assertEquals(len(self.windows.all), 2)
        self.assertEquals(len(self.marionette.chrome_window_handles), 2)
        for handle in self.marionette.chrome_window_handles:
            if handle != first_window.handle:
                self.marionette.switch_to_window(handle)
                break

        second_window = self.windows.current
        self.assertNotEquals(first_window.handle, second_window.handle)

        first_window.switch_to()
        self.assertEquals(first_window.handle,
                          self.marionette.chrome_window_handle)

        self.assertFalse(second_window.closed)
        second_window.close()
        self.assertTrue(second_window.closed)

        self.assertEquals(len(self.windows.all), 1)
        self.assertEquals(len(self.marionette.chrome_window_handles), 1)
        self.assertEquals(first_window.handle,
                          self.marionette.chrome_window_handle)

    def test_browser_window(self):
        self.assertNotEqual(self.browser.dtds, [])
        self.assertNotEqual(self.browser.properties, [])

        self.assertIsNotNone(self.browser.is_private)

        self.assertIsNotNone(self.browser.menubar)
        self.assertIsNotNone(self.browser.navbar)
        self.assertIsNotNone(self.browser.tabbar)
