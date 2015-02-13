# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.marionette import HTMLElement


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

    def __init__(self, marionette_getter, window, element):
        # importing globally doesn't work
        from .ui.windows import BaseWindow

        assert isinstance(window, BaseWindow)
        assert isinstance(element, HTMLElement)

        BaseLib.__init__(self, marionette_getter)
        self._window = window
        self._element = element

    @property
    def element(self):
        """Returns the reference to the underlying DOM element.

        :returns: Reference to the DOM element
        """
        return self._element

    @property
    def window(self):
        """Returns the reference to the chrome window.

        :returns: :class:`BaseWindow` instance of the chrome window.
        """
        return self._window
