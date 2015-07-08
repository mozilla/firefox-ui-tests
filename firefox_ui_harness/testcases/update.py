# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pprint

from . import FirefoxTestCase

from firefox_puppeteer.api.software_update import SoftwareUpdate
from firefox_puppeteer.ui.update_wizard import UpdateWizardDialog


class UpdateTestCase(FirefoxTestCase):

    def __init__(self, *args, **kwargs):
        FirefoxTestCase.__init__(self, *args, **kwargs)

        self.target_buildid = kwargs.pop('update_target_buildid')
        self.target_version = kwargs.pop('update_target_version')

        self.update_channel = kwargs.pop('update_channel')
        self.default_update_channel = None

        self.update_mar_channels = set(kwargs.pop('update_mar_channels'))
        self.default_mar_channels = None

        self.updates = []

    def setUp(self, is_fallback=False):
        FirefoxTestCase.setUp(self)
        self.software_update = SoftwareUpdate(lambda: self.marionette)

        # Bug 604364 - Preparation to test multiple update steps
        self.current_update_index = 0

        self.staging_directory = self.software_update.staging_directory

        # If requested modify the default update channel. It will be active
        # after the next restart of the application
        # Bug 1142805 - Modify file via Python directly
        if self.update_channel:
            # Backup the original content and the path of the channel-prefs.js file
            self.default_update_channel = {
                'content': self.software_update.update_channel.file_contents,
                'path': self.software_update.update_channel.file_path,
            }
            self.software_update.update_channel.default_channel = self.update_channel

        # If requested modify the list of allowed MAR channels
        # Bug 1142805 - Modify file via Python directly
        if self.update_mar_channels:
            # Backup the original content and the path of the update-settings.ini file
            self.default_mar_channels = {
                'content': self.software_update.mar_channels.config_file_contents,
                'path': self.software_update.mar_channels.config_file_path,
            }
            self.software_update.mar_channels.add_channels(self.update_mar_channels)

        # Bug 1142805 - Until we don't modify the channel-prefs.js and update-settings.ini
        # files before Firefox gets started, a restart of Firefox is necessary to
        # accept the new update channel.
        self.restart()

        # Dictionary which holds the information for each update
        self.updates = [{
            'build_pre': self.software_update.build_info,
            'build_post': None,
            'fallback': is_fallback,
            'patch': {},
            'success': False,
        }]

        self.assertEqual(self.software_update.update_channel.default_channel,
                         self.software_update.update_channel.channel)

        self.assertTrue(self.update_mar_channels.issubset(
                        self.software_update.mar_channels.channels))

        # Check if the user has permissions to run the update
        self.assertTrue(self.software_update.allowed)

    def assert_update_applied(self, update_status):
        """Checks if an update has been applied correctly.

        :param update_status: All the data collected during the update process
        """
        # Get the information from the last update
        info = update_status[self.current_update_index]

        # The upgraded version should be identical with the version given by
        # the update and we shouldn't have run a downgrade
        check = self.marionette.execute_script("""
          Components.utils.import("resource://gre/modules/Services.jsm");

          return  Services.vc.compare(arguments[0], arguments[1]);
        """, script_args=[info['build_post']['version'], info['build_pre']['version']])

        self.assertGreaterEqual(check, 0, 'The version of the upgraded build is higher or equal')

        # If a target version has been specified, check if it matches the updated build
        if self.target_version:
            self.assertEqual(info['build_post']['version'], self.target_version)

        # The post buildid should be identical with the buildid contained in the patch
        self.assertEqual(info['build_post']['buildid'], info['patch']['buildid'])

        # If a target buildid has been specified, check if it matches the updated build
        if self.target_buildid:
            self.assertEqual(info['build_post']['buildid'], self.target_buildid)

        # An upgrade should not change the builds locale
        self.assertEqual(info['build_post']['locale'], info['build_pre']['locale'])

        # Check that no application-wide add-ons have been disabled
        self.assertEqual(info['build_post']['disabled_addons'],
                         info['build_pre']['disabled_addons'])

    def check_update_applied(self):
        self.updates[self.current_update_index]['build_post'] = self.software_update.build_info

        about_window = self.browser.open_about_window()
        try:
            update_available = about_window.check_for_updates()

            # No further updates should be offered now with the same update type
            if update_available:
                about_window.download(wait_for_finish=False)

                self.assertNotEqual(self.software_update.active_update.type,
                                    self.updates[self.current_update_index].type)

            # Check that updates have been applied correctly
            self.assert_update_applied(self.updates)

            self.updates[self.current_update_index]['success'] = True

        finally:
            about_window.close()

    def download_and_apply_available_update(self, force_fallback=False):
        """Checks, downloads, and applies an available update.

        :param force_fallback: Optional, if `True` invalidate current update status.
         Defaults to `False`.
        """
        # Open the about window and check for updates
        about_window = self.browser.open_about_window()

        try:
            update_available = about_window.check_for_updates()
            self.assertTrue(update_available)

            # Download update and wait until it has been applied
            about_window.download()
            about_window.wait_for_update_applied()

        finally:
            self.updates[self.current_update_index]['patch'] = about_window.patch_info

        if force_fallback:
            # Set the downloaded update into failed state
            self.software_update.force_fallback()

        # Restart Firefox to apply the downloaded update
        self.restart()

    def download_and_apply_forced_update(self):
        # The update wizard dialog opens automatically after the restart
        dialog = self.windows.switch_to(lambda win: type(win) is UpdateWizardDialog)

        # In case of a broken complete update the about window has to be used
        if self.updates[self.current_update_index]['patch']['is_complete']:
            about_window = None
            try:
                self.assertEqual(dialog.wizard.selected_panel,
                                 dialog.wizard.error)
                dialog.close()

                # Open the about window and check for updates
                about_window = self.browser.open_about_window()
                update_available = about_window.check_for_updates()
                self.assertTrue(update_available)

                # Download update and wait until it has been applied
                about_window.download()
                about_window.wait_for_update_applied()

            finally:
                if about_window:
                    self.updates[self.current_update_index]['patch'] = about_window.patch_info

        else:
            try:
                self.assertEqual(dialog.wizard.selected_panel,
                                 dialog.wizard.error_patching)

                # Start downloading the fallback update
                dialog.download()
                dialog.close()

            finally:
                self.updates[self.current_update_index]['patch'] = dialog.patch_info

        # Restart Firefox to apply the update
        self.restart()

    def restore_config_files(self):
        # Reset channel-prefs.js file if modified
        try:
            if self.default_update_channel:
                path = self.default_update_channel['path']
                self.logger.info('Restoring channel defaults for: {}'.format(path))
                with open(path, 'w') as f:
                    f.write(self.default_update_channel['content'])
        except IOError:
            self.logger.error('Failed to reset the default update channel.',
                              exc_info=True)

        # Reset update-settings.ini file if modified
        try:
            if self.default_mar_channels:
                path = self.default_mar_channels['path']
                self.logger.info('Restoring mar channel defaults for: {}'.format(path))
                with open(path, 'w') as f:
                    f.write(self.default_mar_channels['content'])
        except IOError:
            self.logger.error('Failed to reset the default mar channels.',
                              exc_info=True)

    def tearDown(self):
        try:
            self.browser.tabbar.close_all_tabs([self.browser.tabbar.selected_tab])

            # Print results for now until we have treeherder integration
            output = pprint.pformat(self.updates)
            self.logger.info('Update test results: \n{}'.format(output))

        finally:
            FirefoxTestCase.tearDown(self)

            self.restore_config_files()
