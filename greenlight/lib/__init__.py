# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import HTMLElement

from .decorators import use_class_as_property


class Puppeteer(object):
    """The puppeteer class is used to expose libraries to test cases.

    Each library can be referenced by its puppeteer name as a member of a
    FirefoxTestCase instance. For example, from within a test method, the
    "current_window" member of the "Browser" class can be accessed via
    "self.browser.current_window".
    """
    client = None

    def get_client(self):
        return self.client

    def set_client(self, client):
        self.client = client

    @use_class_as_property('api.windows.Windows')
    def windows(self):
        """
        Provides shortcuts to the top-level windows.

        See the :class:`~window.Windows` reference.
        """

    @use_class_as_property('api.keys.Keys')
    def keys(self):
        """
        Provides a definition of control keys to use with keyboard shortcuts.
        For example, keys.CONTROL or keys.ALT.

        See the :class:`~api.keys.Keys` reference.
        """

    @use_class_as_property('api.prefs.DefaultPrefBranch')
    def prefs(self):
        """
        Provides an api for setting and inspecting preferences, as see in
        about:config.

        See the :class:`~api.prefs.DefaultPrefBranch` reference.
        """


class DOMElement(HTMLElement):
    """
    Class that inherits from HTMLElement and provides a way for subclasses to
    expose new api's.
    """

    def __new__(cls, element):
        instance = object.__new__(cls)
        instance.__dict__ = element.__dict__.copy()
        setattr(instance, 'inner', element)

        return instance

    def __init__(self, element):
        pass
