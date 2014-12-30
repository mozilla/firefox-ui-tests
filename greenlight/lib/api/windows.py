# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By
from marionette.errors import NoSuchElementException

from ..base import BaseLib
from ..ui.base_window import BaseWindow


class Windows(BaseLib):

    @property
    def all(self):
        """
        :returns: a list of :class:`BaseWindow`'s corresponding to the
                  windows in `marionette.window_handles`.
        """
        old_handle = self.marionette.chrome_window_handle
        windows = []
        for handle in self.marionette.chrome_window_handles:
            self.marionette.switch_to_window(handle)
            windows.append(self.current)
        self.marionette.switch_to_window(old_handle)
        return windows

    @property
    def current(self):
        """
        :returns: The :class:`BaseWindow` for the currently active window.
        """
        window_element = self.marionette.find_element(By.CSS_SELECTOR, ':root')
        window_type = self.marionette.get_window_type()

        if window_type == 'navigator:browser':
            from ..ui.browser_window import BrowserWindow
            return BrowserWindow(window_element)
        else:
            return BaseWindow(window_element)

    def switch_to(self, target):
        """
        Switches context to the specified window.

        :param target: The window to switch to. `target` can be a
                       :class:`BaseWindow`, a `window_handle` or a callback
                       that returns True in the context of the desired window.
        :returns: The old `window_handle`. This makes it easy to switch back
                  to the original window later.

        The callback is useful for switching to a window for which the handle
        isn't known. For example, say we want to switch to a window that has
        three tabs::

            def test_switch_to_window_with_three_tabs(self):
                def has_three_tabs(window):
                    return window.tabbar and len(window.tabbar.tabs) == 3

                old_handle = self.windows.switch_to(has_three_tabs)
                self.assertTrue(has_three_tabs(self.windows.current))

                # return to the original window
                self.windows.switch_to(old_handle)
        """
        # TODO: If switched failed ensure to select the old window
        if isinstance(target, BaseWindow):
            return target.switch_to()
        elif target in self.marionette.chrome_window_handles:
            return self.marionette.switch_to_window(target)
        elif callable(target):
            # switch if callback returns true. This is useful for when you want
            # to, e.g. switch to the window that contains a certain element.
            old_handle = self.marionette.chrome_window_handle
            for window in self.all:
                window.switch_to()
                if target(window):
                    return old_handle
            self.marionette.switch_to_window(old_handle)

        raise NoSuchElementException("Could not find a window element for '{}'"
                                     .format(target))
