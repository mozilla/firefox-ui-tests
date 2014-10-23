# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase

class TestBackgroundScrolling(MarionetteTestCase):

    def test_background_scrolling(self):
        self.marionette.set_context('chrome')
        tabbrowser = self.marionette.find_element('id', 'tabbrowser-tabs')

        arrowscrollbox = tabbrowser.find_element('anon attribute', {'anonid': 'arrowscrollbox'})
        print(arrowscrollbox.tag_name)

        scrollbox = arrowscrollbox.find_element('anon attribute', {'anonid': 'scrollbox'})
        print(scrollbox.tag_name)
