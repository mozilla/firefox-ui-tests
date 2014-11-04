# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import NoSuchElementException

from . import DOMElement

class MenuPanel(object):
    def __init__(self, client):
        self.client = client

    @property
    def popup(self):
        return MenuPanelElement.create(self.client.find_element('id', 'PanelUI-popup'))
    

class MenuPanelElement(DOMElement):
    _buttons = None

    @property
    def buttons(self):
        if not self._buttons:
            self._buttons = self.find_element('id', 'PanelUI-multiView') \
                                .find_element('anon attribute', {'anonid': 'viewContainer'}) \
                                .find_elements('tag name', 'toolbarbutton')
        return self._buttons
    
    def click(self, target=None):
        """
        Overrides HTMLElement.click to provide a target to click.

        :param target: The label associated with the button to click on, e.g 'New Private Window'.
        :returns: The window id of the preferences window to be used with
        """
        if not target:
            return DOMElement.click(self)

        for button in self.buttons:
            if button.get_attribute('label') == target:
                return button.click()
        raise NoSuchElementException("Could not find '{}' in the menu panel UI".format(target))
