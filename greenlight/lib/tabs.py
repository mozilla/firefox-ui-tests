# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import HTMLElement
from marionette.errors import NoSuchElementException

from .decorators import using_context


class Tabs(object):
    def __init__(self, client):
        self.client = client

    @property
    def newtab_button(self):
        return self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_element('anon attribute', {'anonid': 'tabs-newtab-button'})

    @property
    def active_tab(self):
        for tab in self.tabs:
            # TODO this doesn't work; see bug 1088223
            #if tab.get_attribute('selected'):

            selected = self.client.execute_script("""
                let tab = arguments[0];
                return tab.getAttribute('selected');
            """, script_args=[tab])

            if selected:
                return tab

    @property
    def tabs(self):
        return self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_elements('tag name', 'tab')

    def get_tab(self, target):
        if isinstance(target, int):
            return self.tabs[target]

        if isinstance(target, basestring):
            for tab in self.tabs:
                if target in tab.get_attribute('label'):
                    return tab
            raise NoSuchElementException("Could not find tab with a label containing '{}'".format(target))

        raise TypeError("Invalid type for 'target': {}".format(type(target)))

    def switch_to_tab(self, tab):
        if not isinstance(tab, HTMLElement):
            tab = self.get_tab(tab)

        return tab.click()
