# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import HTMLElement

from .decorators import use_lib_as_property


class Puppeteer(object):
    client = None

    def get_client(self):
        return self.client

    def set_client(self, client):
        self.client = client

    # these libs are for UI manipulation

    @use_lib_as_property('ui.browser.Browser')
    def browser(self):
        """
        Provides shortcuts to the top-level browser windows.
        """

    @use_lib_as_property('ui.menu.MenuBar')
    def menubar(self):
        """
        Provides access to the menu bar area. For example the 'File', 'View'
        and 'Tools' menus.
        """

    @use_lib_as_property('ui.menu.MenuPanel')
    def menupanel(self):
        """
        Provides access to the menu popup. This is the menu opened after
        clicking the settings button on the right hand side of the browser.
        """

    @use_lib_as_property('ui.navbar.NavBar')
    def navbar(self):
        """
        Provides access to the navigation bar. This is the toolbar containing
        the back, forward and home buttons. It also contains the location bar.
        """

    @use_lib_as_property('ui.tabs.Tabs')
    def tabstrip(self):
        """
        Provides access to the tab bar. This is the toolbar containing all the
        tabs and the new tab button.
        """

    # these libs wrap gecko APIs

    @use_lib_as_property('api.keys.Keys')
    def keys(self):
        """
        Provides a definition of control keys to use with keyboard shortcuts.
        For example, keys.CONTROL or keys.ALT.
        """

    @use_lib_as_property('api.l10n.L10n')
    def l10n(self):
        """
        Provides an api for retrieving localized strings for various UI
        widgets.
        """

    @use_lib_as_property('api.prefs.DefaultPrefBranch')
    def prefs(self):
        """
        Provides an api for setting and inspecting preferences, as see in
        about:config.
        """


class DOMElement(HTMLElement):
    """
    Class that inherits from HTMLElement and provides a way for subclasses to
    expose new api's.
    """

    @classmethod
    def create(cls, element):
        instance = object.__new__(cls)
        instance.__dict__ = element.__dict__.copy()
        setattr(instance, 'inner', element)
        return instance
