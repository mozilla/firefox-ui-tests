# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, Wait

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness import FirefoxTestCase


class TestMixedScriptContentBlocking(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.url = 'https://mozqa.com/data/firefox/security/mixed_content_blocked/index.html'
        self.test_elements = [
            ('result1', 'Insecure script one'),
            ('result2', 'Insecure script from iFrame'),
            ('result3', 'Insecure plugin'),
            ('result4', 'Insecure stylesheet'),
        ]
        self.locationbar = self.browser.navbar.locationbar

    def tearDown(self):
        try:
            self.marionette.execute_script("arguments[0].hidePopup();",
                                           script_args=[self.locationbar.notification_popup])
        finally:
            FirefoxTestCase.tearDown(self)

    def _expect_protection_status(self, enabled):
        if enabled:
            color, icon_filename, state = (
                "rgb(0, 136, 0)",
                "identity-icons-https.png",
                "blocked"
            )
        else:
            color, icon_filename, state = (
                "rgb(255, 0, 0)",
                "identity-icons-https-mixed-active.png",
                "unblocked"
            )

        icon_id = "bad-content-%s-notification-icon" % state
        icon = self.marionette.find_element(By.ID, icon_id)
        Wait(self.marionette).until(
            lambda _: icon.get_attribute('showing') == 'true',
            message="The icon should be showing"
        )

        # First call to Wait() needs a longer timeout due to the reload of the web page.
        favicon = self.locationbar.favicon
        Wait(self.marionette, timeout=self.browser.timeout_page_load).until(
            lambda _: icon_filename in favicon.value_of_css_property('list-style-image'),
            message="The correct icon is displayed"
        )

        with self.marionette.using_context('content'):
            for identifier, description in self.test_elements:
                el = self.marionette.find_element(By.ID, identifier)
                Wait(self.marionette).until(
                    lambda mn: el.value_of_css_property('color') == color,
                    message=("%s has been %s" % (description, state))
                )

    def expect_protection_enabled(self):
        self._expect_protection_status(True)

    def expect_protection_disabled(self):
        self._expect_protection_status(False)

    @skip_under_xvfb
    def test_mixed_content_page(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.expect_protection_enabled()

        # TODO: This should consume the ui class for popups when implemented in
        # bug 1144873.
        popup = self.locationbar.notification_popup
        self.assertEqual(popup.get_attribute('state'), 'closed')

        popupbox = self.marionette.find_element(By.ID,
                                                'bad-content-blocked-notification-icon')
        popupbox.click()

        Wait(self.marionette).until(
            lambda _: popup.get_attribute('state') == 'open',
            message="The notification popup should be open"
        )

        notification_element = self.marionette.find_element(By.ID, 'bad-content-notification')

        button_label = self.browser.get_entity('mixedContentBlocked2.options')
        options_button = notification_element.find_element(By.ANON_ATTRIBUTE,
                                                           {'label': button_label})
        options_button.click()

        item_label = self.browser.get_entity('mixedContentBlocked2.unblock.label')
        menu_item = notification_element.find_element(By.ANON_ATTRIBUTE,
                                                      {'label': item_label})
        menu_item.click()

        Wait(self.marionette).until(
            lambda _: popup.get_attribute('state') == 'closed',
            message="The notification popup should be closed"
        )

        self.expect_protection_disabled()

        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.expect_protection_disabled()
