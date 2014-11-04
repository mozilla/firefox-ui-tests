# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from greenlight.harness.decorators import uses_lib
from greenlight.harness.testcase import FirefoxTestCase


class TestL10n(FirefoxTestCase):

    @uses_lib('l10n')
    def test_dtd_entity(self):
        dtds = ['chrome://global/locale/filepicker.dtd',
                'chrome://browser/locale/baseMenuOverlay.dtd']

        value = self.l10n.get_localized_entity(dtds, 'helpSafeMode.label')
        elm = self.marionette.find_element('id', 'helpSafeMode')
        self.assertEqual(value, elm.get_attribute('label'))

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_entity,
                          dtds, 'notExistent')

    @uses_lib('l10n')
    def test_properties(self):
        properties = ['chrome://global/locale/filepicker.properties',
                      'chrome://global/locale/findbar.properties']

        # TODO: Find a way to verify the retrieved translated string
        value = self.l10n.get_localized_property(properties, 'NotFound')
        self.assertNotEqual(value, '')

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_property,
                          properties, 'notExistent')
