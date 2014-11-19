# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import (
    HTMLElement,
    Wait,
)
from marionette.errors import (
    NoSuchElementException,
    StaleElementException,
)

from .. import DOMElement
from ..decorators import using_context
from ..base import BaseLib

class Tabs(BaseLib):

    @property
    def newtab_button(self):
        return self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_element('anon attribute', {'anonid': 'tabs-newtab-button'})

    @property
    def active_tab(self):
        for tab in self.tabs:
            if tab.is_active():
                return tab

    @property
    def tabs(self):
        tabs = self.client.find_element('id', 'tabbrowser-tabs') \
                          .find_elements('tag name', 'tab')
        return [self.TabElement.create(tab) for tab in tabs]

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



    class TabElement(DOMElement):

        def is_active(self):
            """
            Whether the tab is currently active or not.

            :returns: True if the tab is currently selected, otherwise False.
            """
            # TODO this doesn't work; see bug 1088223
            #if tab.get_attribute('selected'):

            return self.marionette.execute_script("""
                let tab = arguments[0];
                return tab.getAttribute('selected');
            """, script_args=[self.inner])

        def close(self):
            """
            Closes the tab.
            """
            close_button = self.find_element('anon', None) \
                               .find_element('class name', 'tab-close-button')
            ret = close_button.click()

            def im_gone(m):
                try:
                    self.tag_name
                    return False
                except StaleElementException:
                    return True
            Wait(self.marionette).until(im_gone)
            return ret
