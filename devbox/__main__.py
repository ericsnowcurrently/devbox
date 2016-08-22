import argparse
import logging
import sys

from .command import Command


def get_logger(verbosity, defaultlevel=2):
    if verbosity is None:
        verbosity = 0

    logger = logging.getLogger(__package__)
    logger.propagate = False

    LOG_LEVELS = {0: logging.CRITICAL,
                  1: logging.WARNING,
                  2: logging.INFO,
                  3: logging.DEBUG,
                  }
    levelnum = verbosity + defaultlevel
    level = LOG_LEVELS[min(max(levelnum, 0),
                           max(LOG_LEVELS))]
    logger.setLevel(level)

    handler = logging.StreamHandler()
    #handler.setFormatter(logging.Formatter())
    logger.addHandler(handler)

    return logger


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
                       indent + 'devbox [-qv] [--dryrun] target',
                       ))
    parser = argparse.ArgumentParser(
        prog='devbox',
        usage=usage,
        description='tools for setting up a dev environment',
        parents=[parent],
        )
    parser.add_argument('--dryrun', action='store_true', default=False,
                        help='show what would have been done')
    parser.add_argument('target',
                        help='the container or host to set up')

    # Parse and post-process the commandline.
    args = parser.parse_args(argv)

    args.verbosity = args.verbose - args.quiet
    del args.verbose
    del args.quiet

    del args.version

    return args


def get_command(args, logger):
    """Return the command that corresponds to the args."""
    cmd = Command(target=args.target,
                  logger=logger,
                  verbosity=args.verbosity,
                  dryrun=args.dryrun,
                  )
    return cmd


def main(args, *, _get_command=get_command):
    """Execute the devbox command."""
    logger = get_logger(args.verbosity)

    cmd = _get_command(args, logger)
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
