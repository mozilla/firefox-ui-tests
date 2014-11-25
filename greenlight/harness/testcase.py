# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase

from greenlight.lib import Puppeteer


class FirefoxTestCase(MarionetteTestCase, Puppeteer):
    """
    Test case that inherits from a Puppeteer object so Firefox specific
    libraries are exposed to test scope.
    """
    def __init__(self, *args, **kwargs):
        MarionetteTestCase.__init__(self, *args, **kwargs)

    def setUp(self, *args, **kwargs):
        MarionetteTestCase.setUp(self, *args, **kwargs)
        self.marionette.set_context('chrome')
        self.set_client(self.marionette)

        self.browser = self.windows.current

    def tearDown(self, *args, **kwargs):
        self.client = None
        MarionetteTestCase.tearDown(self, *args, **kwargs)
