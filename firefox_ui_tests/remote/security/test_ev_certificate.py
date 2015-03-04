# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.errors import NoSuchElementException

from firefox_ui_harness.decorators import skip_if_e10s, skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestEVCertificate(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://ssl-ev.mozqa.com/'

        self.identity_popup = self.browser.navbar.locationbar.identity_popup

    def tearDown(self):
        try:
            self.identity_popup.close(force=True)
            self.windows.close_all([self.browser])
        except NoSuchElementException:
            # TODO: A NoSuchElementException may be thrown here when the test is skipped
            # as under xvfb.
            pass
        finally:
            FirefoxTestCase.tearDown(self)

    @skip_if_e10s
    @skip_under_xvfb
    def test_ev_certificate(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        # Get the information from the certificate
        cert = self.browser.tabbar.selected_tab.certificate
        address = self.security.get_address_from_certificate(cert)

        # Check the identity popup label displays
        self.assertEqual(self.identity_popup.organization_label.get_attribute('value'),
                         cert['organization'])
        self.assertEqual(self.identity_popup.country_label.get_attribute('value'),
                         '(' + address['country'] + ')')

        # Check the favicon
        # TODO: find a better way to check, e.g., mozmill's isDisplayed
        favicon = self.browser.navbar.locationbar.favicon
        self.wait_for_condition(lambda _: favicon.get_attribute('hidden') == 'false')

        # Check the identity popup box
        self.assertEqual(self.identity_popup.box.get_attribute('className'),
                         'verifiedIdentity')

        self.identity_popup.box.click()
        self.wait_for_condition(lambda _: self.identity_popup.is_open)

        # Check the idenity popup doorhanger
        self.assertEqual(self.identity_popup.popup.get_attribute('className'),
                         'verifiedIdentity')

        # Check that the lock icon is visible
        self.assertNotEqual(self.identity_popup.encryption_icon.
                            value_of_css_property('list-style-image'), 'none')

        # Check the certificate's domain name
        # Bug 443116 - Larry strips the 'www.' from the host name using the eTLDservice.
        # This is expected behavior.
        self.assertEqual(self.identity_popup.host.get_attribute('textContent'),
                         self.security.get_domain_from_common_name(cert['commonName']))

        # Check the organization name
        self.assertEqual(self.identity_popup.owner.get_attribute('textContent'),
                         cert['organization'])

        # Check the owner location string
        # More information:
        # hg.mozilla.org/mozilla-central/file/eab4a81e4457/browser/base/content/browser.js#l7012
        location = self.browser.get_property('identity.identified.state_and_country')
        location = location.replace('%S', address['state'], 1).replace('%S', address['country'])
        location = address['city'] + '\n' + location
        self.assertEqual(self.identity_popup.owner_location.get_attribute('textContent'),
                         location)

        # Check the verifier
        l10n_verifier = self.browser.get_property('identity.identified.verifier')
        l10n_verifier = l10n_verifier.replace('%S', cert['issuerOrganization'])
        self.assertEqual(self.identity_popup.verifier.get_attribute('textContent'),
                         l10n_verifier)

        # Check the encryption label
        self.assertEqual(self.identity_popup.encryption_label.get_attribute('textContent'),
                         self.browser.get_property('identity.encrypted2'))

        # Open the Page Info window by clicking the More Information button
        page_info = self.browser.open_page_info_window(
            lambda _: self.identity_popup.more_info_button.click())

        try:
            # Verify that the current panel is the security panel
            self.assertEqual(page_info.deck.selected_panel, page_info.deck.security)

            # Verify the domain listed on the security panel
            self.assertIn(cert['commonName'],
                          page_info.deck.security.domain.get_attribute('value'))

            # Verify the owner listed on the security panel
            self.assertEqual(page_info.deck.security.owner.get_attribute('value'),
                             cert['organization'])

            # Verify the verifier listed on the security panel
            self.assertEqual(page_info.deck.security.verifier.get_attribute('value'),
                             cert['issuerOrganization'])
        finally:
            page_info.close()
            self.browser.focus()
