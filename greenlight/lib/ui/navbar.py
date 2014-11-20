# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class NavBar(BaseLib):

    # TODO location bar, stop/refresh, bookmarks

    @property
    def back_button(self):
        """
        :returns: The back button element.
        """
        return self.client.find_element('id', 'back-button')

    @property
    def forward_button(self):
        """
        :returns: The forward button element.
        """
        return self.client.find_element('id', 'forward-button')

    @property
    def home_button(self):
        """
        :returns: The home button element.
        """
        return self.client.find_element('id', 'home-button')

    @property
    def menu_button(self):
        """
        :returns: The menu button element.
        """
        return self.client.find_element('id', 'PanelUI-menu-button')

    @property
    def location(self):
        """
        :returns: The string in the location bar (usually the current url).
        """
        # TODO probably doesn't work with e10s enabled
        return self.client.execute_script("""
            return gBrowser.selectedBrowser.contentWindow.location.href;
        """)
