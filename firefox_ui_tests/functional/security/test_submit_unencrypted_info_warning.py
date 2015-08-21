# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, expected, Wait

from marionette_driver.errors import NoAlertPresentException
from marionette_driver.marionette import Alert

from firefox_ui_harness import FirefoxTestCase


class TestSubmitUnencryptedInfoWarning(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://ssl-dv.mozqa.com/data/firefox/security/unencryptedsearch.html'
        self.test_string = 'mozilla'

        self.prefs.set_pref('security.warn_submit_insecure', True)

    def test_submit_unencrypted_info_warning(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

            # Get the page's search box and submit button.
            searchbox = self.marionette.find_element(By.ID, 'q')
            button = self.marionette.find_element(By.ID, 'submit')

            # Use the page's search box to submit information.
            searchbox.send_keys(self.test_string)
            button.click()

            # Get the expected warning text and replace its two instances of "##" with "\n\n".
            message = self.browser.get_property('formPostSecureToInsecureWarning.message')
            message = message.replace('##', '\n\n')

            # Wait for the warning, verify the expected text matches warning, accept the warning
            warning = Alert(self.marionette)
            try:
                Wait(self.marionette, ignored_exceptions=NoAlertPresentException).until(
                    lambda _: warning.text == message)
            finally:
                warning.accept()

            # Wait while the page updates
            Wait(self.marionette).until(expected.element_stale(searchbox))

            # Check that search_term contains the test string.
            search_term = self.marionette.find_element(By.ID, 'search-term')
            self.assertEqual(search_term.get_attribute('textContent'), self.test_string)
