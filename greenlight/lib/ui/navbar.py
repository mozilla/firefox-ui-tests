# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class NavBar(BaseLib):

    @property
    def back_button(self):
        return self.client.find_element('id', 'back-button')

    @property
    def forward_button(self):
        return self.client.find_element('id', 'forward-button')

    @property
    def home_button(self):
        return self.client.find_element('id', 'home-button')

    @property
    def menu_button(self):
        return self.client.find_element('id', 'PanelUI-menu-button')

    @property
    def location(self):
        # TODO probably doesn't work with e10s enabled
        return self.client.execute_script("""
            return gBrowser.selectedBrowser.contentWindow.location.href;
        """)
