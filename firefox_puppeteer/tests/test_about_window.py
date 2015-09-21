# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By

from firefox_ui_harness import FirefoxTestCase
from firefox_ui_harness.decorators import skip_under_xvfb


class TestAboutWindow(FirefoxTestCase):

    def tearDown(self):
        try:
            self.windows.close_all([self.browser])
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_under_xvfb
    def test_basic(self):
        self.about_window = self.browser.open_about_window()
        self.assertEqual(self.about_window.window_type, 'Browser:About')

    @skip_under_xvfb
    def test_elements(self):
        """Test correct retrieval of elements."""
        self.about_window = self.browser.open_about_window()
        self.deck = self.about_window.deck

        self.assertNotEqual(self.about_window.dtds, [])

        self.assertEqual(self.deck.element.get_attribute('localName'), 'deck')

        # apply panel
        panel = self.deck.apply
        self.assertEqual(panel.element.get_attribute('localName'), 'hbox')
        self.assertEqual(panel.button.get_attribute('localName'), 'button')

        # apply_billboard panel
        panel = self.deck.apply_billboard
        self.assertEqual(panel.element.get_attribute('localName'), 'hbox')
        self.assertEqual(panel.button.get_attribute('localName'), 'button')

        # check_for_updates panel
        panel = self.deck.check_for_updates
        self.assertEqual(panel.element.get_attribute('localName'), 'hbox')
        self.assertEqual(panel.button.get_attribute('localName'), 'button')

        # checking_for_updates panel
        self.assertEqual(self.deck.checking_for_updates.element.get_attribute('localName'), 'hbox')

        # download_and_install panel
        panel = self.deck.download_and_install
        self.assertEqual(panel.element.get_attribute('localName'), 'hbox')
        self.assertEqual(panel.button.get_attribute('localName'), 'button')

        # download_failed panel
        self.assertEqual(self.deck.download_failed.element.get_attribute('localName'), 'hbox')

        # downloading panel
        self.assertEqual(self.deck.downloading.element.get_attribute('localName'), 'hbox')

    @skip_under_xvfb
    def test_open_window(self):
        """Test various opening strategies."""
        self.about_window = self.browser.open_about_window()

        def opener(win):
            menu = win.marionette.find_element(By.ID, 'aboutName')
            menu.click()

        open_strategies = ('menu',
                           opener,
                           )

        self.about_window.close()
        for trigger in open_strategies:
            about_window = self.browser.open_about_window(trigger=trigger)
            self.assertEquals(about_window, self.windows.current)
            about_window.close()

    @skip_under_xvfb
    def test_patch_info(self):
        self.about_window = self.browser.open_about_window()

        self.assertEqual(self.about_window.patch_info['download_duration'], None)
        self.assertIsNotNone(self.about_window.patch_info['channel'])
