import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest

from pabot import pabot


class TestPabotSuiteNamesIO(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        robot_file = open('{}/test.robot'.format(self.tmpdir), 'w')
        robot_file.write(textwrap.dedent(
        '''
        *** Variables ***
        ${LETSFAIL}  PASS
        *** Test Cases ***
        Test 1
            Should Not Be Equal  ${LETSFAIL}  FAIL
            Log  something
            Set Suite Variable	${LETSFAIL}  FAIL
        Test 2
            Should Not Be Equal  ${LETSFAIL}  FAIL
            Log  something too
            Set Suite Variable	${LETSFAIL}  FAIL
        Test 3
            Should Not Be Equal  ${LETSFAIL}  FAIL
            Log  something three
            Set Suite Variable	${LETSFAIL}  FAIL
        '''))
        robot_file.close()
        def broken_store(hashes, suite_names):
            raise IOError()
        self.original = pabot.store_suite_names
        pabot.store_suite_names = broken_store
        self.original_curdir = os.getcwd()
        os.chdir(self.tmpdir)

    def test_unable_to_write_pabotsuitenames(self):
        names = pabot.solve_suite_names('outs', [self.tmpdir], {}, {'testlevelsplit':True})
        self.assertEqual([n.name[len(self.tmpdir):] for n in names], ['.Test 1', '.Test 2', '.Test 3'])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        pabot.store_suite_names = self.original
        os.chdir(self.original_curdir)

if __name__ == '__main__':
    unittest.main()
