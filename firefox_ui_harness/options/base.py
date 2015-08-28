# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import firefox_puppeteer
import firefox_ui_tests

from marionette import BaseMarionetteOptions


class FirefoxUIOptions(BaseMarionetteOptions):
    def __init__(self, **kwargs):
        BaseMarionetteOptions.__init__(self, **kwargs)

        # Inheriting object must call this __init__ to set up option handling
        self.add_option('--installer',
                        dest='installer',
                        help='Installer of a Gecko application to use for running the tests')
        self.add_option('--workspace',
                        dest='workspace_path',
                        help='Path to use for all temporary data. Defaults to TEMP.')

    def parse_args(self, *args, **kwargs):
        options, tests = BaseMarionetteOptions.parse_args(self, *args, **kwargs)

        # Bug 1142064 - We cannot easily extent options because registered handlers
        # are called at the end in MarionetteBaseOptions.verify_usage(). As result it
        # will abort due to no binary specified. Once the bug is fixed we can move
        # the whole block to self.base_verify_usage().
        if options.installer:
            if options.binary:
                self.error('Options --binary and --installer are mutually exclusive.')

            options.binary = 'FAKED_VALUE'

        tests = tests or [firefox_puppeteer.manifest, firefox_ui_tests.manifest_all]

        return (options, tests)
