# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import Wait
from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness import FirefoxTestCase


class TestLocationBar(FirefoxTestCase):

    def test_reload(self):
        event_types = ["shortcut", "shortcut2", "button"]
        for event in event_types:
            # TODO: Until we have waitForPageLoad, this only tests API
            # compatibility.
            self.browser.navbar.locationbar.reload_url(event, force=True)
            self.browser.navbar.locationbar.reload_url(event, force=False)

    def test_focus_and_clear(self):
        locationbar = self.browser.navbar.locationbar
        locationbar.urlbar.send_keys("zyx")
        locationbar.clear()
        self.assertEqual(locationbar.value, '')
        locationbar.urlbar.send_keys("zyx")
        self.assertEqual(locationbar.value, 'zyx')
        locationbar.clear()
        self.assertEqual(locationbar.value, '')

    def test_load_url(self):
        data_uri = 'data:text/html,<title>Title</title>'
        locationbar = self.browser.navbar.locationbar
        locationbar.load_url(data_uri)

        with self.marionette.using_context('content'):
            Wait(self.marionette).until(lambda mn: mn.get_url() == data_uri)

    def test_urlbar_input(self):
        urlbar_input = self.browser.navbar.locationbar.urlbar_input
        self.assertEqual('input', urlbar_input.get_attribute('localName'))
        self.assertIn('urlbar-input', urlbar_input.get_attribute('className'))

    def test_contextmenu(self):
        contextmenu = self.browser.navbar.locationbar.contextmenu
        self.assertEqual('menupopup', contextmenu.get_attribute('localName'))

    def test_contextment_entry(self):
        contextmenu_entry = self.browser.navbar.locationbar.get_contextmenu_entry('paste')
        self.assertEqual('cmd_paste', contextmenu_entry.get_attribute('cmd'))

    def test_reloadbutton(self):
        reload_button = self.browser.navbar.locationbar.reload_button
        self.assertEqual('toolbarbutton', reload_button.get_attribute('localName'))

    def test_urlbar(self):
        urlbar = self.browser.navbar.locationbar.urlbar
        self.assertEqual('textbox', urlbar.get_attribute('localName'))

    def test_favicon(self):
        favicon = self.browser.navbar.locationbar.favicon
        self.assertEqual('image', favicon.get_attribute('localName'))

    def test_history_drop_marker(self):
        drop_marker = self.browser.navbar.locationbar.history_drop_marker
        self.assertEqual('dropmarker', drop_marker.get_attribute('localName'))

    def test_stopbutton(self):
        stop_button = self.browser.navbar.locationbar.stop_button
        self.assertEqual('toolbarbutton', stop_button.get_attribute('localName'))


class TestAutoCompleteResults(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.browser.navbar.locationbar.clear()

    def tearDown(self):
        try:
            autocompleteresults = self.browser.navbar.locationbar.autocomplete_results
            autocompleteresults.close(force=True)
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
        autocompleteresults = self.browser.navbar.locationbar.autocomplete_results
        self.assertFalse(autocompleteresults.is_open)
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        results = autocompleteresults.results
        Wait(self.marionette).until(lambda _: autocompleteresults.is_open)
        visible_result_count = len(autocompleteresults.visible_results)
        self.assertTrue(visible_result_count > 0)
        self.assertEqual(visible_result_count,
                         int(results.get_attribute('itemCount')))

    @skip_under_xvfb
    def test_close(self):
        autocompleteresults = self.browser.navbar.locationbar.autocomplete_results
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        Wait(self.marionette).until(lambda _: autocompleteresults.is_open)
        # The Wait in the library implementation will fail this if this doesn't
        # end up closing.
        autocompleteresults.close()

    @skip_under_xvfb
    def test_force_close(self):
        autocompleteresults = self.browser.navbar.locationbar.autocomplete_results
        self.browser.navbar.locationbar.urlbar.send_keys('a')
        Wait(self.marionette).until(lambda _: autocompleteresults.is_open)
        # The Wait in the library implementation will fail this if this doesn't
        # end up closing.
        autocompleteresults.close(force=True)

    @skip_under_xvfb
    def test_matching_text(self):
        # The default profile always has links to mozilla.org. So multiple results
        # will be found with 'moz'.
        input_text = 'moz'

        autocompleteresults = self.browser.navbar.locationbar.autocomplete_results
        self.browser.navbar.locationbar.urlbar.send_keys(input_text)
        Wait(self.marionette).until(lambda _: autocompleteresults.is_open)
        visible_results = autocompleteresults.visible_results
        self.assertTrue(len(visible_results) > 0)
        for result in visible_results:
            title_matches = autocompleteresults.get_matching_text(result, "title")
            url_matches = autocompleteresults.get_matching_text(result, "url")
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

    def test_identity_popup_elements(self):
        self.assertEqual(self.identity_popup.box.get_attribute('localName'), 'box')
        self.assertEqual(self.identity_popup.country_label.get_attribute('localName'), 'label')
        self.assertEqual(self.identity_popup.organization_label.get_attribute('localName'),
                         'label')
        self.assertEqual(self.identity_popup.popup.get_attribute('localName'), 'panel')

    @skip_under_xvfb
    def test_popup_elements(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        self.assertEqual(self.identity_popup.encryption_label.get_attribute('localName'),
                         'description')
        self.assertEqual(self.identity_popup.encryption_icon.get_attribute('localName'), 'image')
        self.assertEqual(self.identity_popup.host.get_attribute('localName'), 'description')
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
