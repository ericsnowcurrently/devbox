import argparse


def parse_args(argv=None):
    """Parse the devbox CLI."""

    class VersionAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            from . import __version__
            parser.exit(message=str(__version__) + '\n')

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('-V', '--version', action=VersionAction, nargs=0,
                        help='print the version')
    parent.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase verbosity')
    parent.add_argument('-q', '--quiet', action='count', default=0,
                        help='decrease verbosity')
    parent.add_argument('--dryrun', action='store_true', default=False,
                        help='show what would have been done')

    # Compose the default command.
    indent = ' ' * len('usage: ')
    usage = '\n'.join(('devbox -h | --help',
                       indent + 'devbox -V | --version',
                       indent + 'devbox [-qv] [--dryrun]',
                       ))
    parser = argparse.ArgumentParser(
        prog='devbox',
        usage=usage,
        description='tools for setting up a dev environment',
        parents=[parent],
        )

    # Parse and post-process the commandline.
    args = parser.parse_args(argv)

    args.verbosity = args.verbose - args.quiet
    del args.verbose
    del args.quiet

    del args.version

    return args


def main(args):
    """Execute the devbox command."""
    print(args)


if __name__ == '__main__':
    args = parse_args()
    main(args)
