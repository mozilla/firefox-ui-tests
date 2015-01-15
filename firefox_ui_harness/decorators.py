# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import SkipTest

from firefox_puppeteer.api import appinfo


def skip_if_e10s(target):
    def wrapper(self, *args, **kwargs):
        if self.appinfo.browserTabsRemoteAutostart:
            raise SkipTest("Skipping due to e10s")
        return target(self, *args, **kwargs)
    return wrapper
