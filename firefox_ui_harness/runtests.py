# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import tempfile

import mozfile
import mozinstall
import mozlog
from marionette.runtests import MarionetteHarness, cli as mn_cli

from firefox_ui_harness.arguments import FirefoxUIArguments
from firefox_ui_harness.runners import FirefoxUITestRunner


class FirefoxUIHarness(MarionetteHarness):
    def __init__(self,
                 runner_class=FirefoxUITestRunner,
                 parser_class=FirefoxUIArguments):
        # workaround until next marionette-client release - Bug 1227918
        try:
            MarionetteHarness.__init__(self, runner_class, parser_class)
        except Exception:
            logger = mozlog.commandline.setup_logging('Firefox UI harness', {})
            logger.error('Failure setting up harness', exc_info=True)
            raise

        self.install_folder = None

    def process_args(self):
        # TODO move installer to mozharness script.
        # If the specified binary is an installer it needs to be installed
        if self.args.installer:
            installer = os.path.realpath(self.args.installer)

            if not self.args.workspace:
                self.args.installer_workspace = tempfile.mkdtemp(
                    '.{}'.format(os.path.basename(sys.argv[0]))
                )
            else:
                self.args.installer_workspace = self.args.workspace
            dest_folder = os.path.join(self.args.installer_workspace, 'binary')
            self.args.logger.info(
                'Installing application "%s" to "%s"' % (installer, dest_folder)
            )
            self.install_folder = mozinstall.install(installer, dest_folder)
            self.args.binary = mozinstall.get_binary(self.install_folder,
                                                     'firefox')

    def parse_args(self, *args, **kwargs):
        return MarionetteHarness.parse_args(self, {'mach': sys.stdout})

    def run(self):
        try:
            return MarionetteHarness.run(self)
        finally:
            # Ensure to uninstall the binary if it has been installed before
            if self.install_folder and os.path.exists(self.install_folder):
                self.args.logger.info('Uninstalling application at '
                                      '"%s"' % self.install_folder)
                mozinstall.uninstall(self.install_folder)
            if not self.args.workspace:
                self.args.logger.info(
                    'Removing temporary installer workspace '
                    'at "%s"' % self.args.installer_workspace
                )
                try:
                    mozfile.remove(self.args.installer_workspace)
                except IOError as e:
                    self.logger.error('Cannot remove "%s"' % str(e))


def cli():
    mn_cli(runner_class=FirefoxUITestRunner,
           parser_class=FirefoxUIArguments,
           harness_class=FirefoxUIHarness)

if __name__ == '__main__':
    cli()
