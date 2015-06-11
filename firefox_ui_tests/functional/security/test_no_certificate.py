# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urlparse import urlparse

from marionette_driver import Wait

from firefox_ui_harness.decorators import skip_if_e10s, skip_under_xvfb
from firefox_ui_harness import FirefoxTestCase


class TestNoCertificate(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = self.marionette.absolute_url('layout/mozilla.html')

        self.identity_popup = self.browser.navbar.locationbar.identity_popup

    def tearDown(self):
        try:
            self.windows.close_all([self.browser])
            self.browser.switch_to()
            self.identity_popup.close(force=True)
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_if_e10s
    @skip_under_xvfb
    def test_no_certificate(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        # Check the favicon
        # TODO: find a better way to check, e.g., mozmill's isDisplayed
        favicon_hidden = self.marionette.execute_script("""
          return arguments[0].hasAttribute("hidden");
        """, script_args=[self.browser.navbar.locationbar.favicon])
        self.assertFalse(favicon_hidden, 'The globe favicon is visible')

        # Check that the identity popup organization label is blank
        self.assertEqual(self.identity_popup.organization_label.get_attribute('value'), '',
                         'The favicon has no label')

        self.identity_popup.box.click()
        Wait(self.marionette).until(lambda _: self.identity_popup.is_open)

        # Check the idenity popup doorhanger
        self.assertEqual(self.identity_popup.popup.get_attribute('className'),
                         'unknownIdentity', 'The Larry UI is unknown (aka Grey)')

        # Only the insecure label is visible
        secure_label = self.identity_popup.secure_connection_label
        self.assertEqual(secure_label.value_of_css_property('display'), 'none')

        insecure_label = self.identity_popup.insecure_connection_label
        self.assertNotEqual(insecure_label.value_of_css_property('display'), 'none')

        # Open the Page Info window by clicking the More Information button
        page_info = self.browser.open_page_info_window(
            lambda _: self.identity_popup.more_info_button.click())

        # Verify that the current panel is the security panel
        self.assertEqual(page_info.deck.selected_panel, page_info.deck.security,
                         'The Security tab is selected by default')

        # Check the domain listed on the security panel contains the url's host name
        self.assertIn(urlparse(self.url).hostname,
                      page_info.deck.security.domain.get_attribute('value'),
                      'The domain label contains the host name in the url')

        # Check the owner label equals localized 'securityNoOwner'
        self.assertEqual(page_info.deck.security.owner.get_attribute('value'),
                         page_info.get_property('securityNoOwner'),
                         'The owner label equals the localized "securityNoOwner"')

        # Check the verifier label equals localized 'notset'
        self.assertEqual(page_info.deck.security.verifier.get_attribute('value'),
                         page_info.get_property('notset'),
                         'The verifier label equals the localized "notset"')
