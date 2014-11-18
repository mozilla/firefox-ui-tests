# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import HTMLElement

from .decorators import use_lib_as_property


class Puppeteer(object):
    client = None

    def set_client(self, client):
        self.client = client

    # these libs are for UI manipulation

    @use_lib_as_property('ui.browser.Browser')
    def browser(self):
        pass

    @use_lib_as_property('ui.menu.MenuBar')
    def menubar(self):
        pass

    @use_lib_as_property('ui.menu.MenuPanel')
    def menupanel(self):
        pass

    @use_lib_as_property('ui.navbar.NavBar')
    def navbar(self):
        pass

    @use_lib_as_property('ui.tabs.Tabs')
    def tabstrip(self):
        pass

    # these libs wrap gecko APIs

    @use_lib_as_property('api.keys.Keys')
    def keys(self):
        pass

    @use_lib_as_property('api.l10n.L10n')
    def l10n(self):
        pass

    @use_lib_as_property('api.prefs.DefaultPrefBranch')
    def prefs(self):
        pass


class DOMElement(HTMLElement):

    @classmethod
    def create(cls, element):
        instance = object.__new__(cls)
        instance.__dict__ = element.__dict__.copy()
        setattr(instance, 'inner', element)
        return instance
