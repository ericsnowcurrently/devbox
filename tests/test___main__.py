
import types
import unittest

from devbox.__main__ import parse_args, main


class StubCommand:

    def __init__(self):
        self.calls = []
        self.err = None

    def run(self):
        self.calls.append('run')
        if self.err is not None:
            raise self.err


class TestParseArgs(unittest.TestCase):

    def test_defaults(self):
        args = parse_args()

        self.assertEqual(vars(args),
                         {'dryrun': False, 'verbosity': 0})

    def test_verbose(self):
        args = parse_args(['-vvv'])

        self.assertEqual(args.verbosity, 3)

    def test_quiet(self):
        args = parse_args(['-qqq'])

        self.assertEqual(args.verbosity, -3)

    def test_verbosity_mixed(self):
        args = parse_args(['-qqq', '-vv', '-v' ,'-q', '-vv'])

        self.assertEqual(args.verbosity, 1)

    def test_dryrun(self):
        args = parse_args(['--dryrun'])

        self.assertTrue(args.dryrun)


class TestMain(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.args = types.SimpleNamespace(verbosity=0, dryrun=False)
        self.cmd = StubCommand()

    def _get_command(self, args):
        self.assertIs(args, self.args)
        return self.cmd

    def test_defaults(self):
        result = main(self.args, _get_command=self._get_command)

        self.assertEqual(result, 0)

    def test_verbose_error(self):
        err = Exception('<failed!>')
        self.cmd.err = err
        self.args.verbosity = 1

        with self.assertRaises(Exception) as cm:
            main(self.args, _get_command=self._get_command)

        self.assertIs(cm.exception, err)

    def test_quiet_error(self):
        err = Exception('<failed!>')
        self.cmd.err = err

        result = main(self.args, _get_command=self._get_command)

        self.assertEqual(result, 'ERROR: <failed!>')
