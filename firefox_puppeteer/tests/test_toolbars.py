# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from marionette_driver import expected, By, Wait
from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness import FirefoxTestCase


class TestNavBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.navbar = self.browser.navbar
        self.url = self.marionette.absolute_url('layout/mozilla.html')

        with self.marionette.using_context('content'):
            self.marionette.navigate('about:blank')

        # TODO: check why self.places.remove_all_history() does not work here
        self.marionette.execute_script("""
            let count = gBrowser.sessionHistory.count;
            gBrowser.sessionHistory.PurgeHistory(count);
        """)

    def test_elements(self):
        self.assertEqual(self.navbar.back_button.get_attribute('localName'), 'toolbarbutton')
        self.assertEqual(self.navbar.forward_button.get_attribute('localName'), 'toolbarbutton')
        self.assertEqual(self.navbar.home_button.get_attribute('localName'), 'toolbarbutton')
        self.assertEqual(self.navbar.menu_button.get_attribute('localName'), 'toolbarbutton')
        self.assertEqual(self.navbar.toolbar.get_attribute('localName'), 'toolbar')

    def test_buttons(self):
        self.marionette.set_context('content')

        # Load initial web page
        self.marionette.navigate(self.url)
        Wait(self.marionette).until(expected.element_present(lambda m:
                                    m.find_element(By.ID, 'mozilla_logo')))

        with self.marionette.using_context('chrome'):
            # Both buttons are disabled
            self.assertFalse(self.navbar.back_button.is_enabled())
            self.assertFalse(self.navbar.forward_button.is_enabled())

            # Go to the homepage
            self.navbar.home_button.click()

        Wait(self.marionette).until(expected.element_not_present(lambda m:
                                    m.find_element(By.ID, 'mozilla_logo')))
        self.assertEqual(self.marionette.get_url(), self.browser.default_homepage)

        with self.marionette.using_context('chrome'):
            # Only back button is enabled
            self.assertTrue(self.navbar.back_button.is_enabled())
            self.assertFalse(self.navbar.forward_button.is_enabled())

            # Navigate back
            self.navbar.back_button.click()

        Wait(self.marionette).until(expected.element_present(lambda m:
                                    m.find_element(By.ID, 'mozilla_logo')))
        self.assertEqual(self.marionette.get_url(), self.url)

        with self.marionette.using_context('chrome'):
            # Only forward button is enabled
            self.assertFalse(self.navbar.back_button.is_enabled())
            self.assertTrue(self.navbar.forward_button.is_enabled())

            # Navigate forward
            self.navbar.forward_button.click()

        Wait(self.marionette).until(expected.element_not_present(lambda m:
                                    m.find_element(By.ID, 'mozilla_logo')))
        self.assertEqual(self.marionette.get_url(), self.browser.default_homepage)


class TestLocationBar(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.locationbar = self.browser.navbar.locationbar

    def test_reload(self):
        event_types = ["shortcut", "shortcut2", "button"]
        for event in event_types:
            # TODO: Until we have waitForPageLoad, this only tests API
            # compatibility.
            self.locationbar.reload_url(event, force=True)
            self.locationbar.reload_url(event, force=False)

    def test_focus_and_clear(self):
        self.locationbar.urlbar.send_keys("zyx")
        self.locationbar.clear()
        self.assertEqual(self.locationbar.value, '')

        self.locationbar.urlbar.send_keys("zyx")
        self.assertEqual(self.locationbar.value, 'zyx')

        self.locationbar.clear()
        self.assertEqual(self.locationbar.value, '')

    def test_load_url(self):
        data_uri = 'data:text/html,<title>Title</title>'
        self.locationbar.load_url(data_uri)

        with self.marionette.using_context('content'):
            Wait(self.marionette).until(lambda mn: mn.get_url() == data_uri)

    def test_urlbar_input(self):
        urlbar_input = self.locationbar.urlbar_input
        self.assertEqual('input', urlbar_input.get_attribute('localName'))
        self.assertIn('urlbar-input', urlbar_input.get_attribute('className'))

    def test_contextmenu(self):
        contextmenu = self.locationbar.contextmenu
        self.assertEqual('menupopup', contextmenu.get_attribute('localName'))

    def test_contextment_entry(self):
        contextmenu_entry = self.locationbar.get_contextmenu_entry('paste')
        self.assertEqual('cmd_paste', contextmenu_entry.get_attribute('cmd'))

    def test_reloadbutton(self):
        reload_button = self.locationbar.reload_button
        self.assertEqual('toolbarbutton', reload_button.get_attribute('localName'))

    def test_urlbar(self):
        urlbar = self.locationbar.urlbar
        self.assertEqual('textbox', urlbar.get_attribute('localName'))

    def test_favicon(self):
        favicon = self.locationbar.favicon
        self.assertEqual('image', favicon.get_attribute('localName'))

    def test_history_drop_marker(self):
        drop_marker = self.locationbar.history_drop_marker
        self.assertEqual('dropmarker', drop_marker.get_attribute('localName'))

    def test_stopbutton(self):
        stop_button = self.locationbar.stop_button
        self.assertEqual('toolbarbutton', stop_button.get_attribute('localName'))


class TestAutoCompleteResults(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.browser.navbar.locationbar.clear()

        self.autocomplete_results = self.browser.navbar.locationbar.autocomplete_results

    def tearDown(self):
        try:
            self.autocomplete_results.close(force=True)
        except NoSuchElementException:
            # TODO: A NoSuchElementException is thrown here when tests accessing the
            # autocomplete_results element are skipped.
            pass
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_under_xvfb
    def test_popup_elements(self):
        # TODO: This test is not very robust because it relies on the history
        # in the default profile.
        self.assertFalse(self.autocomplete_results.is_open)
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        results = self.autocomplete_results.results
        Wait(self.marionette).until(lambda _: self.autocomplete_results.is_complete)
        visible_result_count = len(self.autocomplete_results.visible_results)
        self.assertTrue(visible_result_count > 0)
        self.assertEqual(visible_result_count,
                         int(results.get_attribute('itemCount')))

    @skip_under_xvfb
    def test_close(self):
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        Wait(self.marionette).until(lambda _: self.autocomplete_results.is_open)
        # The Wait in the library implementation will fail this if this doesn't
        # end up closing.
        self.autocomplete_results.close()

    @skip_under_xvfb
    def test_force_close(self):
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        Wait(self.marionette).until(lambda _: self.autocomplete_results.is_open)
        # The Wait in the library implementation will fail this if this doesn't
        # end up closing.
        self.autocomplete_results.close(force=True)

    @skip_under_xvfb
    def test_matching_text(self):
        # The default profile always has links to mozilla.org. So multiple results
        # will be found with 'moz'.
        input_text = 'moz'

        self.browser.navbar.locationbar.urlbar.send_keys(input_text)
        Wait(self.marionette).until(lambda _: self.autocomplete_results.is_complete)
        visible_results = self.autocomplete_results.visible_results
        self.assertTrue(len(visible_results) > 0)

        for result in visible_results:
            # check matching text only for results of type bookmark
            if result.get_attribute('type') != 'bookmark':
                continue
            title_matches = self.autocomplete_results.get_matching_text(result, "title")
            url_matches = self.autocomplete_results.get_matching_text(result, "url")
            all_matches = title_matches + url_matches
            self.assertTrue(len(all_matches) > 0)
            for match_fragment in all_matches:
                self.assertIn(match_fragment.lower(), input_text)


class TestIdentityPopup(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.identity_popup = self.browser.navbar.locationbar.identity_popup
        self.url = self.marionette.absolute_url('layout/mozilla.html')

    def tearDown(self):
        try:
            self.identity_popup.close(force=True)
        except NoSuchElementException:
            # TODO: A NoSuchElementException may be thrown here when tests accessing the
            # identity_popup.popup element are skipped.
            pass
        finally:
            FirefoxTestCase.tearDown(self)

    def test_elements(self):
        self.assertEqual(self.identity_popup.box.get_attribute('localName'), 'box')
        self.assertEqual(self.identity_popup.country_label.get_attribute('localName'), 'label')
        self.assertEqual(self.identity_popup.organization_label.get_attribute('localName'),
                         'label')

    @unittest.skip('Bug 1177417 - Lots of failures due to UI changes of the identity popup')
    @skip_under_xvfb
    def test_popup_elements(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        self.assertEqual(self.identity_popup.icon.get_attribute('localName'), 'image')
        self.assertEqual(self.identity_popup.secure_connection_label.get_attribute('localName'),
                         'label')
        self.assertEqual(self.identity_popup.host.get_attribute('localName'), 'label')
        self.assertEqual(self.identity_popup.insecure_connection_label.get_attribute('localName'),
                         'label')
        self.assertEqual(self.identity_popup.more_info_button.get_attribute('localName'),
                         'button')
        self.assertEqual(self.identity_popup.owner.get_attribute('localName'), 'description')
        self.assertEqual(self.identity_popup.owner_location.get_attribute('localName'),
                         'description')
        self.assertEqual(self.identity_popup.permissions.get_attribute('localName'), 'vbox')
        self.assertEqual(self.identity_popup.verifier.get_attribute('localName'), 'description')

    @skip_under_xvfb
    def test_open_close(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.assertFalse(self.identity_popup.is_open)

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        self.identity_popup.close()

        self.assertFalse(self.identity_popup.is_open)

    @skip_under_xvfb
    def test_force_close(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.assertFalse(self.identity_popup.is_open)

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        self.identity_popup.close(force=True)

        self.assertFalse(self.identity_popup.is_open)
