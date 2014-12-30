# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import NoSuchElementException

from ..base import BaseLib
from .. import DOMElement


class MenuBar(BaseLib):
    """
    Class for manipulating the Firefox menubar.
    """

    @property
    def menus(self):
        """
        :returns: A list of :class:`MenuElement`'s corresponding to the top
                  level menus in the menubar.
        """
        menus = self.marionette.find_element('id', 'main-menubar') \
                               .find_elements('tag name', 'menu')
        return [self.MenuElement(menu) for menu in menus]

    def get_menu(self, label):
        """
        Get a MenuElement corresponding to the specified label.

        :param label: The label of the menu, e.g 'File' or 'View'
        :returns: A MenuElement
        """
        menu = [m for m in self.menus if m.get_attribute('label') == label]

        if not menu:
            raise NoSuchElementException("Could not find a menu with label '{}'".format(label))

        return menu[0]

    def select(self, label, item):
        """
        Select an item in a menu.

        :param label: The label of the menu, e.g 'File' or 'View'
        :param item: The label of the item in the menu, e.g 'New Tab'
        """
        return self.get_menu(label).select(item)

    class MenuElement(DOMElement):
        """
        Wraps a menu element.
        """

        @property
        def items(self):
            """
            :returns: A list of menuitem elements within this menu.
            """
            return self.find_element('tag name', 'menupopup') \
                       .find_elements('tag name', 'menuitem')

        def select(self, label):
            """
            Click on a menuitem within this menu.

            :param label: The label of the menuitem, e.g 'New Tab'
            """
            item = [l for l in self.items if l.get_attribute('label') == label]

            if not item:
                raise NoSuchElementException("Could not find an item labeled '{}' in the '{}' menu".format(label, self.get_attribute('label')))

            return item[0].click()
