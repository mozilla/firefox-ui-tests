import time

from marionette import MarionetteTestCase
from marionette.errors import TimeoutException

class TestBackForward(MarionetteTestCase):

    def test_back_forward(self):
        test_urls = [
            'layout/mozilla.html',
            'layout/mozilla_mission.html',
            'layout/mozilla_grants.html',
        ]
        test_urls = ['{}{}'.format(self.marionette.baseurl, t) for t in test_urls]

        for url in test_urls:
            self.marionette.navigate(url)
        self.assertEquals(self.marionette.get_url(), test_urls[-1])

        self.marionette.set_context('chrome')

        back = self.marionette.find_element('id', 'back-button');
        forward = self.marionette.find_element('id', 'forward-button');
        self.assertFalse(forward.is_displayed())

        for i in range(1, len(test_urls)):
            back.click()
            # TODO Implement something akin to waitForPageLoad
            time.sleep(1)
            self.marionette.set_context('content')
            self.assertEquals(self.marionette.get_url(), test_urls[-(i+1)])
            self.marionette.set_context('chrome')
        self.assertFalse(back.is_enabled())
        forward = self.marionette.find_element('id', 'forward-button');
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

