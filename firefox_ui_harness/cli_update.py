# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.runners import UpdateTestRunner
from firefox_ui_harness.runtests import cli
from firefox_ui_harness.options import UpdateOptions


def cli_update():
    cli(runner_class=UpdateTestRunner, parser_class=UpdateOptions)


if __name__ == '__main__':
    cli_update()
