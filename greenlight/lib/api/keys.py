# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import marionette

class Keys(marionette.keys.Keys):
    """Proxy to marionette's keys with an "accel" provided for convenience
    testing across platforms."""

    def __init__(self, client_getter):
        self.client_getter = client_getter

    @property
    def ACCEL(self):
        if self.client_getter().session_capabilities['platformName'] == 'DARWIN':
            return self.META
        return self.CONTROL
