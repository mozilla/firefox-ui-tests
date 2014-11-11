# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from . import using_context

class Tabs(object):
    def __init__(self, client):
        self.client = client

    @property
    @using_context('chrome')
    def active_tab(self):
        # TODO this doesn't work; see bug 1088223
        for tab in self.tabs:
            if tab.get_attribute('selected'):
                return tab

    @property
    @using_context('chrome')
    def tabs(self):
        return self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_elements('tag name', 'tab')

    @property
    @using_context('chrome')
    def newtab_button(self):
        return self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_element('anon attribute', {'anonid': 'tabs-newtab-button'})
