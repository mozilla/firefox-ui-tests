# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import firefox_puppeteer
import firefox_ui_tests

from marionette import BaseMarionetteArguments


class FirefoxUIBaseArguments(object):
    name = 'Firefox UI Tests'
    args = []

    def parse_args_handler(self, args):
        # If no tests are specified fall back to puppeteer unit and all firefox ui tests
        args.tests = args.tests or [firefox_puppeteer.manifest, firefox_ui_tests.manifest_all]


class FirefoxUIArguments(BaseMarionetteArguments):

    def __init__(self, **kwargs):
        BaseMarionetteArguments.__init__(self, **kwargs)

        self.register_argument_container(FirefoxUIBaseArguments())
