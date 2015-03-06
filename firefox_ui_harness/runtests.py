# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
import os
import sys
import tempfile

import mozinstall

from marionette import (BaseMarionetteOptions,
                        BaseMarionetteTestRunner,)
from mozlog import structured

import firefox_puppeteer
import firefox_ui_tests

from .default_prefs import default_prefs
from .testcase import FirefoxTestCase


class FirefoxUIOptions(BaseMarionetteOptions):

    def __init__(self, **kwargs):
        BaseMarionetteOptions.__init__(self, **kwargs)

        self.add_option('--installer',
                        dest='installer',
                        action='store',
                        help='installer of a Gecko application to use for running the tests')

    def parse_args(self, *args, **kwargs):
        options, test_files = BaseMarionetteOptions.parse_args(self, *args, **kwargs)

        # It is not allowed to specify both options for binary and installer
        if options.installer:
            if options.binary:
                self.error('options --binary and --installer are mutually exclusive')

            # Spoofing so verify_usage() is not showing a failure
            options.binary = 'to_be_set'

        if not test_files:
            test_files = [firefox_puppeteer.manifest, firefox_ui_tests.manifest]
        return (options, test_files)


class FirefoxUITestRunner(BaseMarionetteTestRunner):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('server_root'):
            kwargs['server_root'] = firefox_ui_tests.resources

        prefs = kwargs.get('prefs', {})
        runner_prefs = copy.deepcopy(default_prefs)
        runner_prefs.update(prefs)
        kwargs['prefs'] = runner_prefs

        BaseMarionetteTestRunner.__init__(self, *args, **kwargs)
        self.test_handlers = [FirefoxTestCase]


def startTestRunner(runner_class, options, tests):
    install_folder = None

    try:
        # If the specified binary is an installer it needs to be installed
        if options.installer:
            installer = os.path.realpath(options.installer)

            dest_folder = tempfile.mkdtemp()
            options.logger.info('Installing build "%s" to "%s"...' % (installer,
                                                                      dest_folder))
            install_folder = mozinstall.install(installer, dest_folder)
            options.binary = mozinstall.get_binary(install_folder, 'firefox')

        runner = runner_class(**vars(options))
        runner.run_tests(tests)

    finally:
        # Ensure to uninstall the binary if it has been installed before
        if install_folder and os.path.exists(install_folder):
            options.logger.info('Uninstalling build at "%s"...' % install_folder)
            mozinstall.uninstall(install_folder)

    return runner


def cli(runner_class=FirefoxUITestRunner, parser_class=FirefoxUIOptions):
    parser = parser_class(usage='%prog [options] test_file_or_dir <test_file_or_dir> ...')
    structured.commandline.add_logging_group(parser)
    options, tests = parser.parse_args()
    parser.verify_usage(options, tests)

    logger = structured.commandline.setup_logging(
        options.logger_name, options, {'mach': sys.stdout})

    options.logger = logger

    runner = startTestRunner(runner_class, options, tests)
    if runner.failed > 0:
        sys.exit(10)


if __name__ == '__main__':
    sys.exit(cli())
