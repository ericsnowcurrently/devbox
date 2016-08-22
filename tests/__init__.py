import os.path
import sys


TEST_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(TEST_ROOT)

DATA_DIR = os.path.join(TEST_ROOT, '.data')


sys.path.insert(0, PROJECT_ROOT)
