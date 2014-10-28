# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from greenlight.harness.testcase import FirefoxTestCase


class TestL10n(FirefoxTestCase):

    def test_dtd_entity(self):
        dtds = ['chrome://global/locale/filepicker.dtd',
                'chrome://branding/locale/brand.dtd']

        value = self.l10n.get_localized_entity(dtds, 'vendorShortName')
        self.assertEqual(value, 'Mozilla')

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_entity,
                          dtds, 'notExistent')

    def test_properties(self):
        properties = ['chrome://global/locale/filepicker.properties',
                      'chrome://branding/locale/brand.properties']

        value = self.l10n.get_localized_property(properties, 'vendorShortName')
        self.assertEqual(value, 'Mozilla')

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_property,
                          properties, 'notExistent')
