# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

from marionette import (
    BaseMarionetteTestRunner,
    MarionetteTestCase,
)
from marionette.runtests import cli

from .arguments import ReleaseTestParser
from m20s import tests


class ReleaseTestRunner(BaseMarionetteTestRunner):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('server_root'):
            kwargs['server_root'] = tests.resources
        BaseMarionetteTestRunner.__init__(self, *args, **kwargs)
        self.test_handlers = [MarionetteTestCase]


def run():
    cli(runner_class=ReleaseTestRunner, parser_class=ReleaseTestParser)


if __name__ == '__main__':
    sys.exit(run())
