# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from marionette_driver import By, Wait

from ..windows import BaseWindow
from ..update_wizard import UpdateWizardDialog
from ...api.software_update import SoftwareUpdate
from .deck import Deck


class AboutWindow(BaseWindow):
    """Representation of the About window."""
    window_type = 'Browser:About'

    dtds = [
        'chrome://branding/locale/brand.dtd',
        'chrome://browser/locale/aboutDialog.dtd',
    ]

    TIMEOUT_UPDATE_APPLY = 300
    TIMEOUT_UPDATE_CHECK = 30
    TIMEOUT_UPDATE_DOWNLOAD = 360

    def __init__(self, *args, **kwargs):
        BaseWindow.__init__(self, *args, **kwargs)

        self._software_update = SoftwareUpdate(lambda: self.marionette)
        self._download_duration = None

    @property
    def deck(self):
        """The :class:`Deck` instance which represents the deck.

        :returns: Reference to the deck.
        """
        self.switch_to()

        deck = self.window_element.find_element(By.ID, 'updateDeck')
        return Deck(lambda: self.marionette, self, deck)

    @property
    def patch_info(self):
        """ Returns information about the active update in the queue.

        :returns: A dictionary with information about the active patch
        """
        patch = self._software_update.patch_info
        patch['download_duration'] = self._download_duration

        return patch

    def check_for_updates(self):
        """Clicks on "Check for Updates" button, and waits for check to complete.

        :returns: True, if an update is available.
        """
        assert self.deck.selected_panel == self.deck.check_for_updates

        self.deck.check_for_updates.button.click()
        Wait(self.marionette, timeout=self.TIMEOUT_UPDATE_CHECK).until(
            lambda _: self.deck.selected_panel not in
            (self.deck.check_for_updates, self.deck.checking_for_updates),
            message='Check for updates has been finished.')

        return self.deck.selected_panel != self.deck.no_updates_found

    def download(self, wait_for_finish=True, timeout=TIMEOUT_UPDATE_DOWNLOAD):
        """ Download the update.

        :param wait_for_finish: Optional, if True the function has to wait
        for the download to be finished, default to `True`
        :param timeout: Optional, How long to wait for the download to finish,
        default to 360 seconds
        """
        if self.deck.selected_panel == self.deck.download_and_install:
            self.deck.download_and_install.button.click()

            # Wait for the download to start
            Wait(self.marionette).until(
                lambda _: self.deck.selected_panel != self.deck.download_and_install)

        # If there are incompatible addons, handle the old software update dialog
        if self.deck.selected_panel == self.deck.apply_billboard:
            # Clicking the update button will open the old update wizard dialog
            wizard = self.browser.open_window(callback=lambda _: self.deck.update_button.click(),
                                              expected_window_class=UpdateWizardDialog)
            Wait(self.marionette).until(
                lambda _: wizard.deck.selected_panel == wizard.deck.updates_found_basic)

            wizard.download()
            wizard.close()

            self._download_duration = wizard.download_duration
            return

        if wait_for_finish:
            start_time = datetime.now()
            self.wait_for_download_finished(timeout)
            self._download_duration = (datetime.now() - start_time).total_seconds()

    def wait_for_download_finished(self, timeout=TIMEOUT_UPDATE_DOWNLOAD):
        """ Waits until download is completed.

        :param timeout: Optional, How long to wait for the download to finish,
        default to 360 seconds
        """
        Wait(self.marionette, timeout=timeout).until(
            lambda _: self.deck.selected_panel not in
            (self.deck.download_and_install, self.deck.downloading),
            message='Download has been completed.')

        assert self.deck.selected_panel != self.deck.download_failed,\
            'Update has been downloaded'

    def wait_for_update_applied(self, timeout=TIMEOUT_UPDATE_APPLY):
        """ Waits until the downloaded update has been applied.

        :param timeout: Optional, How long to wait for the update to apply,
        default to 300 seconds
        """
        Wait(self.marionette, timeout=timeout).until(
            lambda _: self.deck.selected_panel == self.deck.apply,
            message='Final wizard page has been selected.')

        # Wait for update to be staged because for update tests we modify the update
        # status file to enforce the fallback update. If we modify the file before
        # Firefox does, Firefox will override our change and we will have no fallback update.
        Wait(self.marionette, timeout=timeout).until(
            lambda _: 'applied' in self._software_update.active_update.state,
            message='Update has been applied.')
