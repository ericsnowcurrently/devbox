

class BaseCommand:
    """The common functionality of commands."""

    ATTRS = ['verbosity']

    def __init__(self, *, verbosity=0):
        self._verbosity = verbosity

    def __repr__(self):
        args = ', '.join('{}={!r}'.format(attr, getattr(self, attr))
                         for attr in self.ATTRS)
        return '{}({})'.format(self.__class__.__name__, args)

    @property
    def verbosity(self):
        return self._verbosity

    def run(self):
        """Run the command."""
        raise NotImplementedError


class Command(BaseCommand):
    """A single command."""

    ATTRS = BaseCommand.ATTRS + ['dryrun', 'target']

    def __init__(self, target, *, dryrun=False, **kwargs):
        super().__init__(**kwargs)
        self._target = target
        self._dryrun = dryrun

    @property
    def target(self):
        return self._target

    @property
    def dryrun(self):
        return self._dryrun

    def run(self):
        """Run the command."""
        print(self)
