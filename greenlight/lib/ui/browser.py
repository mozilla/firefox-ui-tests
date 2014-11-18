# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import NoSuchElementException
from marionette.keys import Keys

from ..base import BaseLib
from .. import DOMElement

class Browser(BaseLib):

    @property
    def windows(self):
        old_handle = self.client.current_window_handle
        windows = []
        for handle in self.client.window_handles:
            self.client.switch_to_window(handle)
            windows.append(self.current_window)
        self.client.switch_to_window(old_handle)
        return windows

    @property
    def current_window(self):
        return self.WindowElement.create(self.client.find_element('id', 'main-window'))

    def switch_to_window(self, target):
        if isinstance(target, self.WindowElement):
            return target.switch_to()
        elif target in self.client.window_handles:
            return self.client.switch_to_window(target)
        elif callable(target):
            # switch if callback returns true. This is useful for when you want to, e.g,
            # switch to the window that contains a certain element.
            old_handle = self.client.current_window_handle
            for window in self.windows:
                window.switch_to()
                if target():
                    return old_handle
            self.client.switch_to_window(old_handle)
        raise NoSuchElementException("Could not find a window element for '{}'".format(target))


    class WindowElement(DOMElement):
        keymap = {
         'ctrl': Keys.CONTROL,
         'alt': Keys.ALT,
         'shift': Keys.SHIFT,
         'cmd': Keys.COMMAND,
         'meta': Keys.META,
        }

        @classmethod
        def create(cls, element):
            instance = object.__new__(cls)
            instance.__dict__ = element.__dict__.copy()
            setattr(instance, 'inner', element)
            setattr(instance, 'handle', instance.marionette.current_window_handle)
            return instance

        def send_shortcut(self, shortcut):
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

        def switch_to(self):
            old_handle = self.marionette.current_window_handle
            if self.handle != old_handle:
                self.marionette.switch_to_window(self.handle)
            return old_handle
