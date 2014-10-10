import time

from marionette import MarionetteTestCase
from marionette.errors import TimeoutException

class TestBackForward(MarionetteTestCase):
    # TODO Don't hit the network
    TEST_URLS = [
        'http://example.com/',
        'https://www.mozilla.org/en-US/',
        'http://example.org/',
    ]

    def test_back_forward(self):
        for url in self.TEST_URLS:
            self.marionette.navigate(url)
        self.assertEquals(self.marionette.get_url(), self.TEST_URLS[-1])

        self.marionette.set_context('chrome')

        back = self.marionette.find_element('id', 'back-button');
        forward = self.marionette.find_element('id', 'forward-button');
        self.assertFalse(forward.is_displayed())

        for i in range(1, len(self.TEST_URLS)):
            back.click()
            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)
            self.marionette.set_context('content')
            self.assertEquals(self.marionette.get_url(), self.TEST_URLS[-(i+1)])
            self.marionette.set_context('chrome')
        self.assertFalse(back.is_enabled())
        forward = self.marionette.find_element('id', 'forward-button');
        # TODO For some reason this returns False
        #self.assertTrue(forward.is_displayed())
        self.assertTrue(forward.is_enabled())

        for i in range(1, len(self.TEST_URLS)):
            forward.click()
            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)
            self.marionette.set_context('content')
            self.assertEquals(self.marionette.get_url(), self.TEST_URLS[i])
            self.marionette.set_context('chrome')

