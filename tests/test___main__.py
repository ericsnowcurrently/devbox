
import unittest

from devbox.__main__ import parse_args, main


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

    def test_(self):
        pass
