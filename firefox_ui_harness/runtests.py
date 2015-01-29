# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
import sys

from marionette import BaseMarionetteTestRunner
from marionette.runtests import cli

import firefox_ui_tests

from .arguments import ReleaseTestParser
from .default_prefs import default_prefs
from .testcase import FirefoxTestCase


class ReleaseTestRunner(BaseMarionetteTestRunner):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('server_root'):
            kwargs['server_root'] = firefox_ui_tests.resources

        prefs = kwargs.get('prefs', {})
        runner_prefs = copy.deepcopy(default_prefs)
        runner_prefs.update(prefs)
        kwargs['prefs'] = runner_prefs

        BaseMarionetteTestRunner.__init__(self, *args, **kwargs)
        self.test_handlers = [FirefoxTestCase]


def run():
    cli(runner_class=ReleaseTestRunner, parser_class=ReleaseTestParser)


if __name__ == '__main__':
    sys.exit(run())
