# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase
from puppeteer import Puppeteer

class FirefoxTestCase(MarionetteTestCase):
    """
    Test case that adds a Puppeteer object to test scope.
    """
    def __init__(self, *args, **kwargs):
        MarionetteTestCase.__init__(self, *args, **kwargs)
        self.puppeteer = Puppeteer()

    def setUp(self, *args, **kwargs):
        MarionetteTestCase.setUp(self, *args, **kwargs)
        self.puppeteer.set_client(self.marionette)

    def tearDown(self, *args, **kwargs):
        self.puppeteer.client = None
        MarionetteTestCase.tearDown(self, *args, **kwargs)

