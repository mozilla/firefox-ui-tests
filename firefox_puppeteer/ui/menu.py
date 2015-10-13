# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By
from marionette_driver.errors import NoSuchElementException

from firefox_puppeteer import DOMElement
from firefox_puppeteer.base import BaseLib


class MenuBar(BaseLib):
    """Wraps the menubar DOM element inside a browser window."""

    @property
    def menus(self):
        """A list of :class:`MenuElement` instances corresponding to
        the top level menus in the menubar.

        :returns: A list of :class:`MenuElement` instances.
        """
        menus = (self.marionette.find_element(By.ID, 'main-menubar')
                                .find_elements(By.TAG_NAME, 'menu'))
        return [self.MenuElement(menu) for menu in menus]

    def get_menu(self, label):
        """Get a :class:`MenuElement` instance corresponding to the specified label.

        :param label: The label of the menu, e.g., **File** or **View**.
        :returns: A :class:`MenuElement` instance.
        """
        menu = [m for m in self.menus if m.get_attribute('label') == label]

        if not menu:
            raise NoSuchElementException('Could not find a menu with '
                                         'label "{}"'.format(label))

        return menu[0]

    def select(self, label, item):
        """Select an item in a menu.

        :param label: The label of the menu, e.g., **File** or **View**.
        :param item: The label of the item in the menu, e.g., **New Tab**.
        """
        return self.get_menu(label).select(item)

    class MenuElement(DOMElement):
        """Wraps a menu element DOM element."""

        @property
        def items(self):
            """A list of menuitem DOM elements within this :class:`MenuElement` instance.

            :returns: A list of items in the menu.
            """
            return (self.find_element(By.TAG_NAME, 'menupopup')
                        .find_elements(By.TAG_NAME, 'menuitem'))

        def select(self, label):
            """Click on a menu item within this menu.

            :param label: The label of the menu item, e.g., **New Tab**.
            """
            item = [l for l in self.items if l.get_attribute('label') == label]

            if not item:
                message = ("Item labeled '{}' not found in the '{}' menu"
                           .format(label, self.get_attribute('label')))
                raise NoSuchElementException(message)

            return item[0].click()
