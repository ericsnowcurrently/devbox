
import logging


class BaseCommand:
    """The common functionality of commands."""

    ATTRS = ['logger', 'verbosity']

    def __init__(self, *, logger=None, verbosity=0):
        if logger is None:
            logger = logging.getLogger(__name__)

        self._logger = logger
        self._verbosity = verbosity

    def __repr__(self):
        args = ', '.join('{}={!r}'.format(attr, getattr(self, attr))
                         for attr in self.ATTRS)
        return '{}({})'.format(self.__class__.__name__, args)

    @property
    def logger(self):
        return self._logger

    @property
    def verbosity(self):
        return self._verbosity

    def run(self):
        """Run the command."""
        raise NotImplementedError


class Command(BaseCommand):
    """A single command."""

    ATTRS = BaseCommand.ATTRS + ['dryrun']

    def __init__(self, *, dryrun=False, **kwargs):
        super().__init__(**kwargs)
        self._dryrun = dryrun

    @property
    def dryrun(self):
        return self._dryrun

    def run(self):
        """Run the command."""
        self.logger.info(str(self))
