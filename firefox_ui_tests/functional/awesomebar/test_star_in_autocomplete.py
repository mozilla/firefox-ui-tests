# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


class TestStarInAutocomplete(FirefoxTestCase):
    """ This replaces
    http://hg.mozilla.org/qa/mozmill-tests/file/default/firefox/tests/functional/testAwesomeBar/testSuggestBookmarks.js
    Check a star appears in autocomplete list for a bookmarked page.
    """

    PREF_LOCATION_BAR_SUGGEST = 'browser.urlbar.default.behavior'

    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.clear_history()

        # Location bar suggests 'History and Bookmarks'
        self.prefs.set_pref(self.PREF_LOCATION_BAR_SUGGEST, 0)

    def tearDown(self):
        FirefoxTestCase.tearDown(self)

        self.prefs.reset_pref(self.PREF_LOCATION_BAR_SUGGEST)

    def clear_history(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate('about:blank')

        self.marionette.execute_script('''
            let count = gBrowser.sessionHistory.count;
            gBrowser.sessionHistory.PurgeHistory(count);
        ''')

    @skip_under_xvfb
    def test_star_in_autocomplete(self):
        search_string = 'grants'

        with self.marionette.using_context('content'):
            self.marionette.navigate(self.marionette.absolute_url('layout/mozilla_grants.html'))

        self.browser.menubar.select('Bookmarks', 'Bookmark This Page')
        done_button = self.marionette.find_element('id', 'editBookmarkPanelDoneButton')
        done_button.click()

        self.clear_history()

        locationbar = self.browser.navbar.locationbar
        # TODO: Replace with visited observer when places module is available
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1121731
        # The data for autocomplete does not load immediately and we cannot wait for an observer
        # until the bug 1121731 is complete
        time.sleep(4)
        locationbar.clear()
        locationbar.urlbar.send_keys(search_string)
        autocomplete_results = locationbar.autocomplete_results

        self.wait_for_condition(lambda mn: locationbar.value == search_string)
        self.wait_for_condition(lambda mn: autocomplete_results.is_open)
        self.wait_for_condition(lambda mn: len(autocomplete_results.visible_results) == 1)

        first_result = autocomplete_results.visible_results[0]
        matching_title = autocomplete_results.get_matching_text(first_result, 'title')[0]
        self.assertEqual(
            search_string.lower(),
            matching_title.lower(),
            'The page title matches the highlighted text')
        self.assertEqual('bookmark',
                         first_result.get_attribute('type'),
                         'The auto-complete result is a bookmark')
