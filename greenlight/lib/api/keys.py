# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import marionette

class Keys(marionette.keys.Keys):
    """Proxy to marionette's keys with an "accel" provided for convenience
    testing across platforms."""

    def __init__(self, client):
        if client.session_capabilities['platformName'] == 'DARWIN':
            self.ACCEL = self.META
        else:
            self.ACCEL = self.CONTROL
