# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import Wait

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestDVCertificate(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.url = 'https://ssl-dv.mozqa.com'
        self.locationbar = self.browser.navbar.locationbar
        self.identity_popup = self.browser.navbar.locationbar.identity_popup

    def tearDown(self):
        try:
            self.browser.switch_to()
            self.identity_popup.close(force=True)
            self.windows.close_all([self.browser])
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_under_xvfb
    def test_dv_cert(self):

        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        cert = self.browser.tabbar.selected_tab.certificate

        favicon_hidden = self.marionette.execute_script("""
          return arguments[0].hasAttribute("hidden");
        """, script_args=[self.locationbar.favicon])

        self.assertFalse(favicon_hidden, 'The page proxy favicon should be visible')

        self.assertIn('identity-icons-https',
                      self.locationbar.favicon.value_of_css_property('list-style-image'),
                      'There is a lock icon')

        self.assertEqual(self.identity_popup.box.get_attribute('className'),
                         'verifiedDomain',
                         'Identity is verified')

        self.identity_popup.box.click()
        Wait(self.marionette).until(
            lambda _: self.identity_popup.is_open,
            message='The popup should be open'
        )

        self.assertEqual(self.identity_popup.popup.get_attribute('className'),
                         'verifiedDomain',
                         'The Larry UI is domain verified (aka Blue)')

        encryption_icon = self.identity_popup.encryption_icon
        self.assertNotEqual(encryption_icon.value_of_css_property('list-style-image'),
                            'none',
                            'There is a lock icon')

        # Bug 443116
        # Larry strips the 'www.' from the CName using the eTLDService
        # This is expected behaviour for the time being
        self.assertEqual(self.identity_popup.host.get_attribute('textContent'),
                         self.security.get_domain_from_common_name(cert['commonName']),
                         'The site identifier string is equal to the cert host')

        verifier_label = self.browser.get_property('identity.identified.verifier')
        self.assertEqual(self.identity_popup.verifier.get_attribute('textContent'),
                         verifier_label.replace("%S", cert['issuerOrganization']),
                         'The "Verified by: %S" string is set')

        def opener(mn):
            self.identity_popup.more_info_button.click()

        page_info_window = self.browser.open_page_info_window(opener)
        deck = page_info_window.deck

        self.assertEqual(deck.selected_panel, deck.security,
                         "The security tab is selected by default")

        self.assertEqual(deck.security.domain.get_attribute('value'),
                         cert['commonName'],
                         "Expected web site label found")

        self.assertEqual(deck.security.owner.get_attribute('value'),
                         page_info_window.get_property('securityNoOwner'),
                         "Expected owner label found")

        self.assertEqual(deck.security.verifier.get_attribute('value'),
                         cert['issuerOrganization'])
