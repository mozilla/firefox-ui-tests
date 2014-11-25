# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys

from .. import DOMElement
from ..api.l10n import L10n


class BaseWindow(DOMElement):
    """Base class for any available chrome window type."""

    # l10n class attributes will be set by each window class individually
    dtds = []
    properties = []

    keymap = {
        'ctrl': Keys.CONTROL,
        'alt': Keys.ALT,
        'shift': Keys.SHIFT,
        'cmd': Keys.COMMAND,
        'meta': Keys.META,
    }

    def __new__(cls, element):
        return DOMElement.__new__(cls, element)

    def __init__(self, element):
        # Due to __new__ we don't have to call __init__ of the super class

        self.handle = self.marionette.current_window_handle
        self.l10n = L10n(lambda: self.marionette)

    @property
    def closed(self):
        """Returns true if the window has been closed."""
        return self.handle not in self.marionette.window_handles

    @property
    def menubar(self):
        """Provides access to the menu bar. For example the 'File' menu.

        See the :class:`~ui.menu.MenuBar` reference.
        """
        from menu import MenuBar
        return MenuBar(lambda: self.marionette)

    @property
    def window(self):
        """Returns the inner DOM window element."""
        return self.inner

    def get_localized_entity(self, entity_id):
        """Returns the localized string for the specified DTD entity id.

        :param entity_id: The id to retrieve the value from.

        :returns: The localized string for the requested entity.

        :raises MarionetteException: When entity id is not found.
        """
        return self.l10n.get_localized_entity(self.dtds, entity_id)

    def get_localized_property(self, property_id):
        """Returns the localized string for the specified property id.

        :param property_id: The id to retrieve the value from.

        :returns: The localized string for the requested property.

        :raises MarionetteException: When property id is not found.
        """
        return self.l10n.get_localized_entity(self.dtds, property_id)

    def send_shortcut(self, shortcut):
        """Sends a keyboard shortcut to the window

        :param shortcut: The shortcut to send. For example `ctrl-w` or
                         `ctrl-shift-t`.
        """
        platform = self.marionette.session_capabilities['platformName'].lower()
        modifiers, key = shortcut.rsplit('-', 1)

        keys = []
        for mod in modifiers.split('-'):
            mod = mod.lower()
            if mod == 'ctrl' and platform == 'darwin':
                mod = 'cmd'
            keys.append(self.keymap[mod])
        keys.append(key.lower())

        self.send_keys(*keys)

    def close(self):
        """Closes the window.

        If this is the last remaining window, the marionette session is ended.
        """
        old_handle = self.switch_to()
        num_windows = len(self.marionette.window_handles)
        return_to = None
        if old_handle != self.handle:
            return_to = old_handle

        ret = self.marionette.close()

        if num_windows > 1 and not return_to:
            return_to = self.marionette.window_handles[0]

        if return_to:
            self.marionette.switch_to_window(return_to)

        return ret

    def open(self):
        # TODO: To be implemented by calling window.open() and observer
        # notifications for the newly opened window
        pass

    def switch_to(self):
        """Switches to this browser window."""
        old_handle = self.marionette.current_window_handle
        if self.handle != old_handle:
            self.marionette.switch_to_window(self.handle)

        return old_handle
