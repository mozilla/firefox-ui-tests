# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from base_window import BaseWindow

from ..decorators import use_class_as_property


class BrowserWindow(BaseWindow):
    """Representation for browser window."""

    window_type = 'navigator:browser'

    dtds = [
        'chrome://branding/locale/brand.dtd',
        'chrome://browser/locale/aboutPrivateBrowsing.dtd',
        'chrome://browser/locale/browser.dtd',
    ]

    properties = [
        'chrome://branding/locale/brand.properties',
        'chrome://branding/locale/browserconfig.properties',
        'chrome://browser/locale/browser.properties',
        'chrome://browser/locale/preferences/preferences.properties',
    ]

    def __init__(self, element):
        BaseWindow.__init__(self, element)

    @property
    def is_private(self):
        """Returns True if it is a Private Browsing window."""
        return self.marionette.execute_script("""
            Cu.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

            let chromeWindow = arguments[0].ownerDocument.defaultView;
            return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
        """, script_args=[self.window])

    @use_class_as_property('ui.navbar.NavBar')
    def navbar(self):
        """
        Provides access to the navigation bar. This is the toolbar containing
        the back, forward and home buttons. It also contains the location bar.

        See the :class:`~ui.navbar.NavBar` reference.
        """

    @use_class_as_property('ui.tabbar.Tabs')
    def tabbar(self):
        """
        Provides access to the tab bar. This is the toolbar containing all the
        tabs, the new tab button, and the tab menu

        See the :class:`~ui.tabbar.Tabs` reference.
        """

    def open(self):
        # TODO: To be implemented
        pass
