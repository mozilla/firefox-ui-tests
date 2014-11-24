# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.errors import TimeoutException

from greenlight.harness.testcase import FirefoxTestCase
from greenlight.harness.decorators import uses_lib


class TestBackForward(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.test_urls = [
            'layout/mozilla.html',
            'layout/mozilla_mission.html',
            'layout/mozilla_grants.html',
        ]
        self.test_urls = [self.marionette.absolute_url(t) for t in self.test_urls]

        with self.marionette.using_context('content'):
            for url in self.test_urls:
                self.marionette.navigate(url)
            self.assertEquals(self.marionette.get_url(), self.test_urls[-1])

    def test_back_forward(self):
        back = self.navbar.back_button
        forward = self.navbar.forward_button
        self.assertFalse(forward.is_displayed())

        for i in range(1, len(self.test_urls)):
            back.click()

            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)

            with self.marionette.using_context('content'):
                self.assertEquals(self.marionette.get_url(),
                                  self.test_urls[-(i + 1)])

        self.assertFalse(back.is_enabled())
        forward = self.navbar.forward_button
        # TODO For some reason this returns False
        #self.assertTrue(forward.is_displayed())
        self.assertTrue(forward.is_enabled())

        for i in range(1, len(self.test_urls)):
            forward.click()

            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)

            with self.marionette.using_context('content'):
                self.assertEquals(self.marionette.get_url(), self.test_urls[i])
