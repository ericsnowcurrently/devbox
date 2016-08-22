import argparse
import sys

from .command import Command


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
    parser.add_argument('--dryrun', action='store_true', default=False,
                        help='show what would have been done')

    # Parse and post-process the commandline.
    args = parser.parse_args(argv)

    args.verbosity = args.verbose - args.quiet
    del args.verbose
    del args.quiet

    del args.version

    return args


def get_command(args):
    """Return the command that corresponds to the args."""
    cmd = Command(verbosity=args.verbosity,
                  dryrun=args.dryrun,
                  )
    return cmd


def main(args, *, _get_command=get_command):
    """Execute the devbox command."""
    cmd = _get_command(args)
    try:
        cmd.run()
    except Exception as e:
        if args.verbosity <= 0:
            return 'ERROR: {}'.format(e)
        raise
    return 0


if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args))
