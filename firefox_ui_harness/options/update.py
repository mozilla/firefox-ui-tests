# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import FirefoxUIOptions


class UpdateOptions(FirefoxUIOptions):
    def __init__(self, **kwargs):
        FirefoxUIOptions.__init__(self, **kwargs)

        # Inheriting object must call this __init__ to set up option handling
        group = self.add_option_group('Update Tests')
        group.add_option('--update-allow-mar-channel',
                         dest='update_mar_channels',
                         default=[],
                         action='append',
                         metavar='MAR_CHANNEL',
                         help='Additional MAR channel to be allowed for updates, '
                              'e.g. "firefox-mozilla-beta" for updating a release '
                              'build to the latest beta build.')
        group.add_option('--update-channel',
                         dest='update_channel',
                         metavar='CHANNEL',
                         help='Channel to use for the update check.')
        group.add_option('--update-direct-only',
                         dest='update_direct_only',
                         default=False,
                         action='store_true',
                         help='Only perform a direct update')
        group.add_option('--update-fallback-only',
                         dest='update_fallback_only',
                         default=False,
                         action='store_true',
                         help='Only perform a fallback update')
        group.add_option('--update-override-url',
                         dest='update_override_url',
                         metavar='URL',
                         help='Force specified URL to use for update checks.')
        group.add_option('--update-target-version',
                         dest='update_target_version',
                         metavar='VERSION',
                         help='Version of the updated build.')
        group.add_option('--update-target-buildid',
                         dest='update_target_buildid',
                         metavar='BUILD_ID',
                         help='Build ID of the updated build.')

    def parse_args(self, *args, **kwargs):
        options, tests = FirefoxUIOptions.parse_args(self, *args, **kwargs)

        return (options, tests)

    def verify_usage(self, options, tests):
        if options.update_direct_only and options.update_fallback_only:
            self.error('Options --update-direct-only and --update-fallback-only '
                       'are mutually exclusive.')

        FirefoxUIOptions.verify_usage(self, options, tests)
