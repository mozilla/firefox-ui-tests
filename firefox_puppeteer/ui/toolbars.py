# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait, By

from ..api.keys import Keys
from ..api.l10n import L10n
from ..base import BaseLib
from ..decorators import use_class_as_property


class NavBar(BaseLib):
    """ The NavBar class provides access to elements contained in the
    navigation bar as well as the locationbar.
    """

    @property
    def back_button(self):
        """ Provides access to the back button from the navbar ui.

        :returns: The back button element.
        """
        return self.marionette.find_element('id', 'back-button')

    @property
    def forward_button(self):
        """ Provides access to the forward button from the navbar ui.

        :returns: The forward button element.
        """
        return self.marionette.find_element('id', 'forward-button')

    @property
    def home_button(self):
        """ Provides access to the home button from the navbar ui.

        :returns: The home button element.
        """
        return self.marionette.find_element('id', 'home-button')

    @use_class_as_property('ui.toolbars.LocationBar')
    def locationbar(self):
        """Provides members for accessing and manipulationg the
        locationbar.

        See the :class:`~ui.toolbars.LocationBar` reference.
        """

    @property
    def menu_button(self):
        """ Provides access to the menu button from the navbar ui.

        :returns: The menu button element.
        """
        return self.marionette.find_element('id', 'PanelUI-menu-button')


class LocationBar(BaseLib):
    """Various utilities for interacting with the location bar (the text area
    of the ui that typically displays the current url).
    """

    dtds = ["chrome://branding/locale/brand.dtd",
            "chrome://browser/locale/browser.dtd"]

    def __init__(self, *args, **kwargs):
        BaseLib.__init__(self, *args, **kwargs)
        # TODO: A "utility" module that sets up the client directly would be
        # useful here.
        self.l10n = L10n(self.get_marionette)
        self.keys = Keys(self.get_marionette)

    @use_class_as_property('ui.toolbars.AutocompleteResults')
    def autocomplete_results(self):
        """Provides utility members for accessing and manipulationg the
        locationbar.

        See the :class:`~ui.toolbars.AutocompleteResults` reference.
        """

    def clear(self):
        """ Clears the contents of the url bar (via the DELETE shortcut).
        """
        self.focus('shortcut')
        self.urlbar.send_keys(Keys.DELETE)
        Wait(self.marionette).until(
            lambda _: self.urlbar.get_attribute('value') == '')

    def close_context_menu(self):
        """ Closes the Location Bar context menu by a key event.
        """
        # TODO: This method should be implemented via the menu API.
        self.contextmenu.send_keys(Keys.ESCAPE)

    @property
    def contextmenu(self):
        """ Provides access to the urlbar context menu.

        :returns: The urlbar contextmenu element.
        """
        parent = self.urlbar.find_element('anon attribute', {'anonid': 'textbox-input-box'})
        return parent.find_element('anon attribute', {'anonid': 'input-box-contextmenu'})

    @property
    def favicon(self):
        """ Provides asccess to the urlbar favicon.

        :returns: The favicon element.
        """
        return self.marionette.find_element(By.ID, 'page-proxy-favicon')

    def focus(self, evt='click'):
        """Focus the location bar according to the provided event.

        :param evt: The event to synthesize in order to focus the urlbar
                    (one of 'click' or 'shortcut').
        """
        if evt == 'click':
            self.urlbar.click()
        elif evt == 'shortcut':
            cmd_key = self.l10n.get_entity(LocationBar.dtds, 'openCmd.commandkey')
            (self.marionette.find_element(By.ID, 'main-window')
                            .send_keys(self.keys.ACCEL, cmd_key))
        else:
            raise ValueError("An unknown event type was passed: %s" % evt)

        Wait(self.marionette).until(
            lambda _: self.urlbar.get_attribute('focused') == 'true')

    def get_contextmenu_entry(self, action):
        """ Retirieves the urlbar context menu entry corresponding
        to the given action.

        :param action: The action correspoding to the retrieved value.
        :returns: The urlbar contextmenu entry.
        """
        # TODO: This method should be implemented via the menu API.
        entries = self.contextmenu.find_elements('css selector', 'menuitem')
        filter_on = 'cmd_%s' % action
        found = [e for e in entries if e.get_attribute('cmd') == filter_on]
        return found[0] if len(found) else None

    @property
    def history_drop_marker(self):
        """ Provides asccess to the history drop marker.

        :returns: The history drop marker.
        """
        return self.urlbar.find_element('anon attribute', {'anonid': 'historydropmarker'})

    @use_class_as_property('ui.toolbars.IdentityPopup')
    def identity_popup(self):
        """Provides utility members for accessing and manipulationg the
        locationbar.

        See the :class:`~ui.toolbars.IdentityPopup` reference.
        """

    def load_url(self, url):
        """Load the specified url in the location bar by synthesized
        keystrokes.

        :param url: The url to load.
        """
        self.clear()
        self.focus('shortcut')
        self.urlbar.send_keys(url + Keys.ENTER)

    @property
    def notification_popup(self):
        """ Provides asccess to the notification popup.

        :returns: The notification popup.
        """
        return self.marionette.find_element(By.ID, "notification-popup")

    @property
    def reload_button(self):
        """ Provides asccess to the reload button.

        :returns: The reload button.
        """
        return self.marionette.find_element(By.ID, 'urlbar-reload-button')

    def reload_url(self, trigger='button', force=False):
        """Reload the currently open page.

        :param trigger: The event type to use to cause the reload. (one of
                        "shortcut", "shortcut2", or "button").
        :param force: Whether to cause a forced reload.
        """
        # TODO: The force parameter is ignored for the moment. Use
        # mouse event modifiers or actions when they're ready.
        # Bug 1097705 tracks this feature in marionette.
        if trigger == 'button':
            self.reload_button.click()
        elif trigger == 'shortcut':
            cmd_key = self.l10n.get_entity(LocationBar.dtds, 'reloadCmd.commandkey')
            self.urlbar.send_keys(cmd_key)
        elif trigger == 'shortcut2':
            self.urlbar.send_keys(self.keys.F5)

    @property
    def stop_button(self):
        """ Provides asccess to the stop button.

        :returns: The stop button.
        """
        return self.marionette.find_element(By.ID, 'urlbar-stop-button')

    @property
    def urlbar(self):
        """ Provides access to the urlbar element.

        :returns: The urlbar element.
        """
        return self.marionette.find_element(By.ID, 'urlbar')

    @property
    def urlbar_input(self):
        """ Provides access to the urlbar input element.

        :returns: The urlbar_input element
        """
        return self.urlbar.find_element('anon attribute', {'anonid': 'input'})

    @property
    def value(self):
        """ Provides access to the currently displayed value of the urlbar.

        :returns: The urlbar value.
        """
        return self.urlbar.get_attribute('value')


class AutocompleteResults(BaseLib):
    """Library for interacting with autocomplete results.
    """

    def __init__(self, *args, **kwargs):
        BaseLib.__init__(self, *args, **kwargs)
        # TODO: A "utility" module that sets up the client directly would be
        # useful here.
        self.l10n = L10n(self.get_marionette)
        self.keys = Keys(self.get_marionette)

    def close(self, force=False):
        """ Closes the urlbar autocomplete popup.

        :param force: If true, the popup is closed by its own hide function,
                      otherwise a key event is sent to close the popup.
        """
        if not self.is_open:
            return

        if force:
            self.marionette.execute_script("""
              arguments[0].hidePopup();
            """, script_args=[self.popup])
        else:
            (self.marionette.find_element('id', 'urlbar')
                            .send_keys(Keys.ESCAPE))
        Wait(self.marionette).until(
            lambda _: not self.is_open)

    def get_matching_text(self, result, match_type):
        """Retuns an array of strings of the matching text within a autocomplete
        result in the urlbar.

        :param result: The result to inspect for matches.
        :param match_type: The type of match to search for (one of "title", "url").
        """

        if match_type == 'title':
            descnode = self.marionette.execute_script("""
              return arguments[0].boxObject.firstChild.childNodes[1].childNodes[0];
            """, script_args=[result])
        elif match_type == 'url':
            descnode = self.marionette.execute_script("""
              return arguments[0].boxObject.lastChild.childNodes[2].childNodes[0];
            """, script_args=[result])
        else:
            raise ValueError('match_type provided must be one of'
                             '"title" or "url", not %s' % match_type)

        return self.marionette.execute_script("""
          let rv = [];
          for (let node of arguments[0].childNodes) {
            if (node.nodeName == 'span') {
              rv.push(node.innerHTML);
            }
          }
          return rv;
        """, script_args=[descnode])

    @property
    def visible_results(self):
        """ Supplies the list of visible autocomplete result nodes.

        :returns: The list of visible results.
        """
        return self.marionette.execute_script("""
          let rv = [];
          let node = arguments[0];
          for (let i = 0; i < node.itemCount; ++i) {
            let item = node.getItemAtIndex(i);
            if (!item.hasAttribute("collapsed")) {
              rv.push(item);
            }
          }
          return rv;
        """, script_args=[self.results])

    @property
    def is_open(self):
        """ Returns whether this popup is currently open.

        :returns: True when the popup is open, otherwise false.
        """
        return self.popup.get_attribute('state') == 'open'

    @property
    def popup(self):
        """ Provides access to the popup result element.

        :returns: The popup result element.
        """
        return self.marionette.find_element(By.ID,
                                            'PopupAutoCompleteRichResult')

    @property
    def results(self):
        """ Povides access to the container node for autocomplete results.

        :returns: The result container node.
        """
        return self.popup.find_element('anon attribute',
                                       {'anonid': 'richlistbox'})


class IdentityPopup(BaseLib):
    """Library wrapping selectors for interacting with the identity popup.
    """

    @property
    def box(self):
        return self.marionette.find_element(By.ID, 'identity-box')

    @property
    def country_label(self):
        return self.marionette.find_element(By.ID, 'identity-icon-country-label')

    @property
    def encryption_label(self):
        return self.marionette.find_element(By.ID, 'identity-popup-encryption-label')

    @property
    def encryption_icon(self):
        return self.marionette.find_element(By.ID, 'identity-popup-encryption-icon')

    @property
    def host(self):
        return self.marionette.find_element(By.ID, 'identity-popup-content-host')

    @property
    def is_open(self):
        """ Returns whether this popup is currently open.

        :returns: True when the popup is open, otherwise false.
        """
        return self.popup.get_attribute('state') == 'open'

    @property
    def more_info_button(self):
        return self.marionette.find_element(By.ID, 'identity-popup-more-info-button')

    @property
    def organization_label(self):
        return self.marionette.find_element(By.ID, 'identity-icon-label')

    @property
    def owner(self):
        return self.marionette.find_element(By.ID, 'identity-popup-content-owner')

    @property
    def owner_location(self):
        return self.marionette.find_element(By.ID, 'identity-popup-content-supplemental')

    @property
    def popup(self):
        return self.marionette.find_element(By.ID, 'identity-popup')

    @property
    def permissions(self):
        return self.marionette.find_element(By.ID, 'identity-popup-permissions')

    @property
    def verifier(self):
        return self.marionette.find_element(By.ID, 'identity-popup-content-verifier')
