# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import mozinfo
from marionette import BaseMarionetteTestRunner

import firefox_ui_tests
from ..testcase import FirefoxTestCase


DEFAULT_PREFS = {
    'app.update.auto': False,
    'app.update.enabled': False,
    'browser.dom.window.dump.enabled': True,
    # Bug 1145668 - Has to be reverted to about:blank once Marionette
    # can correctly handle error pages
    'browser.newtab.url': 'about:newtab',
    'browser.newtabpage.enabled': False,
    'browser.safebrowsing.enabled': False,
    'browser.safebrowsing.malware.enabled': False,
    'browser.search.update': False,
    'browser.sessionstore.resume_from_crash': False,
    'browser.shell.checkDefaultBrowser': False,
    'browser.startup.page': 0,
    'browser.tabs.animate': False,
    'browser.tabs.warnOnClose': False,
    'browser.tabs.warnOnOpen': False,
    'browser.uitour.enabled': False,
    'browser.warnOnQuit': False,
    'datareporting.healthreport.service.enabled': False,
    'datareporting.healthreport.uploadEnabled': False,
    'datareporting.healthreport.documentServerURI': "http://%(server)s/healthreport/",
    'datareporting.healthreport.about.reportUrl': "http://%(server)s/abouthealthreport/",
    'datareporting.policy.dataSubmissionEnabled': False,
    'datareporting.policy.dataSubmissionPolicyAccepted': False,
    'dom.ipc.reportProcessHangs': False,
    'dom.report_all_js_exceptions': True,
    'extensions.enabledScopes': 5,
    'extensions.autoDisableScopes': 10,
    'extensions.getAddons.cache.enabled': False,
    'extensions.installDistroAddons': False,
    'extensions.logging.enabled': True,
    'extensions.showMismatchUI': False,
    'extensions.update.enabled': False,
    'extensions.update.notifyUser': False,
    'focusmanager.testmode': True,
    'geo.provider.testing': True,
    'javascript.options.showInConsole': True,
    'marionette.logging': False,
    'security.notification_enable_delay': 0,
    'signon.rememberSignons': False,
    'startup.homepage_welcome_url': 'about:blank',
    'toolkit.startup.max_resumed_crashes': -1,
    'toolkit.telemetry.enabled': False,
}


class FirefoxUITestRunner(BaseMarionetteTestRunner):
    def __init__(self, **kwargs):
        BaseMarionetteTestRunner.__init__(self, **kwargs)

        if not self.server_root:
            self.server_root = firefox_ui_tests.resources

        # Bug 1146847: This needs a refactoring given that our default
        # preferences are not coming from the command line
        self.prefs.update(DEFAULT_PREFS)

        if not kwargs.get('e10s'):
            self.prefs.update({'browser.tabs.remote.autostart': False})

        self.test_handlers = [FirefoxTestCase]

    def get_application_folder(self, binary):
        """Returns the directory of the application."""
        if mozinfo.isMac:
            end_index = binary.find('.app') + 4
            return binary[:end_index]
        else:
            return os.path.dirname(binary)

    def run_tests(self, tests):
        # Ensure Marionette is always reset before starting tests
        # This might need support in Marionette base
        self.marionette = None
        self.tests = []

        BaseMarionetteTestRunner.run_tests(self, tests)
