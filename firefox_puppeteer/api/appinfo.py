# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class AppInfo(BaseLib):

    @property
    def browserTabsRemoteAutostart(self):
        return self._get_property("browserTabsRemoteAutostart")

    def _get_property(self, prop_name):
        with self.marionette.using_context('chrome'):
            return self.marionette.execute_script("""
              try {
                return Services.appinfo[arguments[0]];
              } catch (e) {
                return null;
              }
            """, script_args=[prop_name])
