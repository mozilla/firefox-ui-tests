# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

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

    def parse_args(self, *args, **kwargs):
        return MarionetteHarness.parse_args(self, {'mach': sys.stdout})


def cli():
    mn_cli(runner_class=FirefoxUITestRunner,
           parser_class=FirefoxUIArguments,
           harness_class=FirefoxUIHarness)

if __name__ == '__main__':
    cli()
