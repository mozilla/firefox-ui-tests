# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

class BaseLib(object):
    """A trivial base class that handles lazily setting the "client" class
    attribute."""

    def __init__(self, client_getter):
        self._client = None
        self._client_getter = client_getter

    @property
    def client(self):
        if self._client is None:
            self._client = self._client_getter()
        return self._client

