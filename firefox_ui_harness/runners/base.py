# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import mozinfo
from marionette import BaseMarionetteTestRunner

import firefox_ui_tests
from ..testcases import FirefoxTestCase


class FirefoxUITestRunner(BaseMarionetteTestRunner):
    def __init__(self, **kwargs):
        BaseMarionetteTestRunner.__init__(self, **kwargs)
        # select the appropriate GeckoInstance
        self.app = 'fxdesktop'
        if not self.server_root:
            self.server_root = firefox_ui_tests.resources

        self.test_handlers = [FirefoxTestCase]

    def get_application_folder(self, binary):
        """Returns the directory of the application."""
        if mozinfo.isMac:
            end_index = binary.find('.app') + 4
            return binary[:end_index]
        else:
            return os.path.dirname(binary)
