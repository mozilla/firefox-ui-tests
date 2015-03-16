# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from marionette_driver import By, Wait

from ..windows import BaseWindow
from ...api.prefs import Preferences
from ...api.software_update import SoftwareUpdate
from .wizard import Wizard


# TODO: Bug 1143020 - Subclass from BaseDialog ui class with possible wizard mixin
class UpdateWizardDialog(BaseWindow):
    """Representation of the old Software Update Wizard Dialog."""
    window_type = 'Update:Wizard'

    dtds = [
        'chrome://branding/locale/brand.dtd',
        'chrome://mozapps/locale/update/updates.dtd',
    ]

    properties = [
        'chrome://branding/locale/brand.properties',
        'chrome://mozapps/locale/update/updates.properties',
    ]

    # For the old update wizard, the errors are displayed inside the dialog. For the
    # handling of updates in the about window the errors are displayed in new dialogs.
    # When the old wizard is open we have to set the preference, so the errors will be
    # shown as expected, otherwise we would have unhandled modal dialogs when errors are raised.
    # See:
    # http://mxr.mozilla.org/mozilla-central/source/toolkit/mozapps/update/nsUpdateService.js?rev=a9240b1eb2fb#4813
    # http://mxr.mozilla.org/mozilla-central/source/toolkit/mozapps/update/nsUpdateService.js?rev=a9240b1eb2fb#4756
    PREF_APP_UPDATE_ALTWINDOWTYPE = 'app.update.altwindowtype'

    TIMEOUT_UPDATE_DOWNLOAD = 360

    def __init__(self, *args, **kwargs):
        BaseWindow.__init__(self, *args, **kwargs)

        self._prefs = Preferences(lambda: self.marionette)
        self._software_update = SoftwareUpdate(lambda: self.marionette)
        self._download_duration = -1

    @property
    def wizard(self):
        """The :class:`Wizard` instance which represents the wizard.

        :returns: Reference to the wizard.
        """
        # The deck is also the root element
        wizard = self.marionette.find_element(By.ID, 'updates')
        return Wizard(lambda: self.marionette, self, wizard)

    @property
    def patch_info(self):
        """ Returns information about the active update in the queue.

        :returns: A dictionary with information about the active patch
        """
        patch = self._software_update.patch_info
        patch['download_duration'] = self._download_duration
        return patch

    def download(self, wait_for_finish=True, timeout=TIMEOUT_UPDATE_DOWNLOAD):
        """ Download the update.

        :param wait_for_finish: Optional, if True the function has to wait
         for the download to be finished, default to `True`
        :param timeout: Optional, How long to wait for the download to finish,
         default to 360 seconds
        """
        self._prefs.set_pref(self.PREF_APP_UPDATE_ALTWINDOWTYPE, self.window_type)

        try:
            channel = self._software_update.update_channel
            assert channel.default_channel == channel.channel, \
                'The update channel has been set correctly. ' \
                'default_channel: is {}, while channel is: {}'.format(
                    self._software_update.update_channel.default_channel,
                    self._software_update.update_channel.channel)

            # If updates have already been found, proceed to download
            if self.wizard.selected_panel in (self.wizard.updates_found_basic,
                                              self.wizard.updates_found_billboard,
                                              self.wizard.error_patching,
                                              ):
                self.select_next_page()

            # If incompatible add-on are installed, skip over the wizard page
            if self.wizard.selected_panel == self.wizard.incompatible_list:
                self.select_next_page()

            # Updates were stored in the cache, so no download is necessary
            if self.wizard.selected_panel in (self.wizard.finished,
                                              self.wizard.finished_background,
                                              ):
                pass

            # Download the update
            elif self.wizard.selected_panel == self.wizard.downloading:
                if wait_for_finish:
                    start_time = datetime.now()
                    self.wait_for_download_finished(timeout)
                    self._download_duration = datetime.now() - start_time

                    Wait(self.marionette).until(
                        lambda _: self.wizard.selected_panel in (self.wizard.finished,
                                                                 self.wizard.finished_background,
                                                                 ),
                        message='Final wizard page has been selected.')

            else:
                raise Exception('Invalid wizard page for downloading an update: {}'.format(
                                self.wizard.selected_panel))

        finally:
            self._prefs.restore_pref(self.PREF_APP_UPDATE_ALTWINDOWTYPE)

    def select_next_page(self):
        """Clicks on "Next" button, and waits for the next page to show up."""
        current_panel = self.wizard.selected_panel

        self.wizard.next_button.click()
        Wait(self.marionette).until(lambda _: self.wizard.selected_panel != current_panel)
