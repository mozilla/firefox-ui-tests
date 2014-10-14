# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import BaseMarionetteOptions

import tests

class ReleaseTestParser(BaseMarionetteOptions):
    
    def parse_args(self, *args, **kwargs):
        options, test_files = BaseMarionetteOptions.parse_args(self, *args, **kwargs)
        if not test_files:
            test_files = [tests.manifest]
        return (options, test_files)
