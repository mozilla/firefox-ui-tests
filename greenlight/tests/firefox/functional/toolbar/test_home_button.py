# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase

class TestHomeButton(MarionetteTestCase):

    def test_home_button(self):
        test_url = '{}layout/mozilla.html'.format(self.marionette.baseurl)
        self.marionette.navigate(url)

        self.marionette.set_context('chrome')
