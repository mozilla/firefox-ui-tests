# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import tempfile

import mozinstall

from mozlog import structured

from firefox_ui_harness.arguments import FirefoxUIArguments
from firefox_ui_harness.runners import FirefoxUITestRunner


def startTestRunner(runner_class, options, tests):
    install_folder = None

    try:
        # Prepare the workspace path so that all temporary data can be stored inside it.
        if options.workspace_path:
            path = os.path.expanduser(options.workspace_path)
            options.workspace = os.path.abspath(path)

            if not os.path.exists(options.workspace):
                os.makedirs(options.workspace)
        else:
            options.workspace = tempfile.mkdtemp('.{}'.format(os.path.basename(sys.argv[0])))

        options.logger.info('Using workspace for temporary data: "{}"'.format(options.workspace))

        # If the specified binary is an installer it needs to be installed
        if options.installer:
            installer = os.path.realpath(options.installer)

            dest_folder = os.path.join(options.workspace, 'binary')
            options.logger.info('Installing application "%s" to "%s"' % (installer,
                                                                         dest_folder))
            install_folder = mozinstall.install(installer, dest_folder)
            options.binary = mozinstall.get_binary(install_folder, 'firefox')

        runner = runner_class(**vars(options))
        runner.run_tests(tests)

    finally:
        # Ensure to uninstall the binary if it has been installed before
        if install_folder and os.path.exists(install_folder):
            options.logger.info('Uninstalling application at "%s"' % install_folder)
            mozinstall.uninstall(install_folder)

    return runner


def cli(runner_class=FirefoxUITestRunner, parser_class=FirefoxUIArguments):
    parser = parser_class(usage='%(prog)s [options] test_file_or_dir <test_file_or_dir> ...')
    structured.commandline.add_logging_group(parser)
    args = parser.parse_args()
    parser.verify_usage(args)

    logger = structured.commandline.setup_logging(
        args.logger_name, args, {'mach': sys.stdout})
    args.logger = logger

    try:
        runner = startTestRunner(runner_class, args, args.tests)
        if runner.failed > 0:
            sys.exit(10)

    except Exception:
        logger.error('Failure during execution of the update test.',
                     exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(cli())
