# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from . import errors


class BaseLib(object):
    """A base class that handles lazily setting the "client" class attribute."""

    def __init__(self, marionette_getter):
        if not callable(marionette_getter):
            raise TypeError('Invalid callback for "marionette_getter": %s' % marionette_getter)

        self._marionette = None
        self._marionette_getter = marionette_getter

    @property
    def marionette(self):
        if self._marionette is None:
            self._marionette = self._marionette_getter()
        return self._marionette

    def get_marionette(self):
        return self.marionette


class UIBaseLib(BaseLib):
    """A base class for all UI element wrapper classes inside a chrome window."""

    def __init__(self, marionette_getter, window):
        BaseLib.__init__(self, marionette_getter)

        # importing globally doesn't work
        from .ui.windows import BaseWindow
        if not isinstance(window, BaseWindow):
            raise errors.UnexpectedWindowTypeError('Not a valid BaseWindow: "%s"' %
                                                   window)
        self._window = window

    @property
    def window(self):
        return self._window
