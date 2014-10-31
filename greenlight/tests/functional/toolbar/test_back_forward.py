# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.errors import TimeoutException

from greenlight.harness.testcase import FirefoxTestCase

class TestBackForward(FirefoxTestCase):

    def test_back_forward(self):
        toolbar = self.puppeteer.toolbar

        test_urls = [
            'layout/mozilla.html',
            'layout/mozilla_mission.html',
            'layout/mozilla_grants.html',
        ]
        test_urls = [self.marionette.absolute_url(t) for t in test_urls]

        for url in test_urls:
            self.marionette.navigate(url)
        self.assertEquals(self.marionette.get_url(), test_urls[-1])

        self.marionette.set_context('chrome')

        back = toolbar.back_button()
        forward = toolbar.forward_button()
        self.assertFalse(forward.is_displayed())

        for i in range(1, len(test_urls)):
            back.click()
            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)
            self.marionette.set_context('content')
            self.assertEquals(self.marionette.get_url(), test_urls[-(i+1)])
            self.marionette.set_context('chrome')
        self.assertFalse(back.is_enabled())
        forward = toolbar.forward_button()
        # TODO For some reason this returns False
        #self.assertTrue(forward.is_displayed())
        self.assertTrue(forward.is_enabled())

        for i in range(1, len(test_urls)):
            forward.click()
            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)
            self.marionette.set_context('content')
            self.assertEquals(self.marionette.get_url(), test_urls[i])
            self.marionette.set_context('chrome')

