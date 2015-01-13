# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from marionette import BaseMarionetteTestRunner
from marionette.runtests import cli

from firefoxtests import tests

from .arguments import ReleaseTestParser
from .testcase import FirefoxTestCase


class ReleaseTestRunner(BaseMarionetteTestRunner):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('server_root'):
            kwargs['server_root'] = tests.resources
        BaseMarionetteTestRunner.__init__(self, *args, **kwargs)
        self.test_handlers = [FirefoxTestCase]


def run():
    cli(runner_class=ReleaseTestRunner, parser_class=ReleaseTestParser)


if __name__ == '__main__':
    sys.exit(run())
