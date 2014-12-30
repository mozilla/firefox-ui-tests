# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class DefaultPrefBranch(BaseLib):
    archive = {}

    @classmethod
    def _cast(cls, value):
        """
        Interpolate a preference from a string.

        - integers will get cast to integers
        - true/false will get cast to True/False
        - anything enclosed in single quotes will be treated as a string with
          the ''s removed from both sides
        """

        if not isinstance(value, basestring):
            return value  # no op
        quote = "'"
        if value == 'true':
            return True
        if value == 'false':
            return False
        try:
            return int(value)
        except ValueError:
            pass
        if value.startswith(quote) and value.endswith(quote):
            value = value[1:-1]
        return value

    def get_pref(self, pref):
        """
        Retrive a preference.

        :param pref: The preference to inspect,e.g
                     browser.tabs.remote.autostart
        :returns: The value of the specified pref.
        """
        with self.marionette.using_context('chrome'):
            value = self.marionette.execute_script("""
              let pref = arguments[0];
              let prefBranch = Cc["@mozilla.org/preferences-service;1"]
                              .getService(Ci.nsIPrefBranch);
              let type = prefBranch.getPrefType(pref);

              switch (type) {
                case prefBranch.PREF_STRING:
                  return prefBranch.getCharPref(pref);
                case prefBranch.PREF_BOOL:
                  return prefBranch.getBoolPref(pref);
                case prefBranch.PREF_INT:
                  return prefBranch.getIntPref(pref);
                case prefBranch.PREF_INVALID:
                  return null;
              }
            """, script_args=[pref])

        return self._cast(value)

    def set_pref(self, pref, value):
        """
        Sets the specified pref to value. Also archives the old value so that
        the pref can be restored with `restore_pref`.

        :param pref: The preference to set.
        :param value: The value to set the preference to.
        """
        with self.marionette.using_context('chrome'):
            self.archive[pref] = self.get_pref(pref)

            ret = self.marionette.execute_script("""
              let pref = arguments[0];
              let value = arguments[1];
              let prefBranch = Cc["@mozilla.org/preferences-service;1"]
                               .getService(Ci.nsIPrefBranch);
              let type = prefBranch.getPrefType(pref);

              switch (type) {
                case prefBranch.PREF_BOOL:
                  prefBranch.setBoolPref(pref, value);
                  break;
                case prefBranch.PREF_STRING:
                  prefBranch.setCharPref(pref, value);
                  break;
                case prefBranch.PREF_INT:
                  prefBranch.setIntPref(pref, value);
                  break;
                default:
                  return false;
              }

              return true;
            """, script_args=[pref, value])

        assert ret

    def restore_pref(self, pref):
        """
        Restore a previously set pref back to its original value.

        :param pref: The preference to restore. It must be a preference that
                     was previously set using `set_pref`.
        """
        return self.set_pref(pref, self.archive[pref])
