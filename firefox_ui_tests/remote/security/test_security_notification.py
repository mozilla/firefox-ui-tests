# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import unittest

from marionette_driver import By
from marionette_driver.errors import MarionetteException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestSecurityNotification(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.urls = [
            # Invalid cert page
            'https://summitbook.mozilla.org',
            # Secure page
            'https://ssl-ev.mozqa.com/',
            # Insecure page
            'http://www.mozqa.com'
        ]

        self.identity_box = self.browser.navbar.locationbar.identity_popup.box

    @unittest.skip('Bug 1106077 - Broken root certificate for http://summitbook.mozilla.org')
    def test_invalid_cert(self):
        with self.marionette.using_context('content'):
            # Go to a site that has an invalid (expired) cert
            self.assertRaises(MarionetteException, self.marionette.navigate, self.urls[0])

            # Wait for the DOM to receive events
            time.sleep(1)

            # Verify the text in Technical Content contains the page with invalid cert
            text = self.marionette.find_element(By.ID, 'technicalContentText')
            self.assertIn(self.urls[0][8:], text.get_attribute('textContent'))

            # Verify the "Get Me Out Of Here!" and "Add Exception" buttons appear
            self.assertIsNotNone(self.marionette.find_element(By.ID, 'getMeOutOfHereButton'))
            self.assertIsNotNone(self.marionette.find_element(By.ID, 'exceptionDialogButton'))

            # Verify the error code is correct
            self.assertIn('sec_error_expired_certificate', text.get_attribute('textContent'))

    def test_secure_website(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.urls[1])

        self.wait_for_condition(lambda _: self.identity_box.get_attribute('className') ==
                                'verifiedIdentity')

    def test_insecure_website(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.urls[2])

        self.wait_for_condition(lambda _: self.identity_box.get_attribute('className') ==
                                'unknownIdentity')
