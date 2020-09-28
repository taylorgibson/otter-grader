####################################
##### Tests for otter generate #####
####################################
import os
import unittest
import subprocess
import json
import shutil

from subprocess import PIPE
from glob import glob
from unittest import mock
from shutil import copyfile

from otter.argparser import get_parser
from otter.generate.autograder import main as autograder
from otter.generate.run_autograder import main as run_autograder

from .. import TestCase

parser = get_parser()

TEST_FILES_PATH = "test/test_generate/test-run-autograder/"

class TestRunAutograder(TestCase):
    def setUp(self):
        super().setUp()

        # env = {"__name__": "__not_main__"}
        with open(TEST_FILES_PATH + "autograder/source/otter_config.json") as f:
            self.config = json.load(f)
        
        # self.config = self.env["config"]
        
        self.expected_results = {
            "tests": [
                {
                    "name": "q1 - 1",
                    "score": 0.0,
                    "max_score": 0.0,
                    "visibility": "visible",
                    "output": "Test case passed!"
                },
                {
                    "name": "q1 - 2",
                    "score": 0.0,
                    "max_score": 0.0,
                    "visibility": "visible",
                    "output": "Test case passed!"
                },
                {
                    "name": "q1 - 3",
                    "score": 0.0,
                    "max_score": 0.0,
                    "visibility": "hidden",
                    "output": "Test case passed!"
                },
                {
                    "name": "q1 - 4",
                    "score": 0.0,
                    "max_score": 0.0,
                    "visibility": "hidden",
                    "output": "Test case passed!"
                },
                {
                    "name": "q2 - 1",
                    "score": 0.0,
                    "max_score": 0.5,
                    "visibility": "visible",
                    "output": "Trying:\n    negate(True)\nExpecting:\n    False\n**********************************************************************\nLine 2, in q2 0\nFailed example:\n    negate(True)\nExpected:\n    False\nGot:\n    True\n"
                },
                {
                    "name": "q2 - 2",
                    "score": 0.0,
                    "max_score": 0.5,
                    "visibility": "visible",
                    "output": "Trying:\n    negate(False)\nExpecting:\n    True\n**********************************************************************\nLine 2, in q2 1\nFailed example:\n    negate(False)\nExpected:\n    True\nGot:\n    False\n"
                },
                {
                    "name": "q2 - 3",
                    "score": 0.0,
                    "max_score": 0.5,
                    "visibility": "hidden",
                    "output": "Trying:\n    negate(\"\")\nExpecting:\n    True\n**********************************************************************\nLine 2, in q2 2\nFailed example:\n    negate(\"\")\nExpected:\n    True\nGot:\n    ''\n"
                },
                {
                    "name": "q2 - 4",
                    "score": 0.0,
                    "max_score": 0.5,
                    "visibility": "hidden",
                    "output": "Trying:\n    negate(1)\nExpecting:\n    False\n**********************************************************************\nLine 2, in q2 3\nFailed example:\n    negate(1)\nExpected:\n    False\nGot:\n    1\n"
                },
                {
                    "name": "q3 - 1",
                    "score": 1.0,
                    "max_score": 1.0,
                    "visibility": "visible",
                    "output": "Test case passed!"
                },
                {
                    "name": "q3 - 2",
                    "score": 1.0,
                    "max_score": 1.0,
                    "visibility": "hidden",
                    "output": "Test case passed!"
                },
                {
                    "name": "q4 - 1",
                    "score": 1.0,
                    "max_score": 1.0,
                    "visibility": "hidden",
                    "output": "Test case passed!"
                },
                {
                    "name": "q6 - 1",
                    "score": 2.5,
                    "max_score": 2.5,
                    "visibility": "visible",
                    "output": "Test case passed!"
                },
                {
                    "name": "q6 - 2",
                    "score": 0.0,
                    "max_score": 2.5,
                    "visibility": "hidden",
                    "output": "Trying:\n    fib = fiberator()\nExpecting nothing\nok\nTrying:\n    for _ in range(10):\n        print(next(fib))\nExpecting:\n    0\n    1\n    1\n    2\n    3\n    5\n    8\n    13\n    21\n    34\n**********************************************************************\nLine 3, in q6 1\nFailed example:\n    for _ in range(10):\n        print(next(fib))\nExpected:\n    0\n    1\n    1\n    2\n    3\n    5\n    8\n    13\n    21\n    34\nGot:\n    0\n    1\n    1\n    1\n    2\n    3\n    5\n    8\n    13\n    21\n"
                },
                {
                    "name": "q7 - 1",
                    "score": 1.0,
                    "max_score": 1.0,
                    "visibility": "visible",
                    "output": "Test case passed!"
                }
            ]
        }

    def test_run_autograder(self):

        # #generate the zip file 
        # generate_command = ["generate", "autograder",
        #     "-t", TEST_FILES_PATH + "tests",
        #     "-o", TEST_FILES_PATH,
        #     "-r", TEST_FILES_PATH + "requirements.txt",
        #     TEST_FILES_PATH + "data/test-df.csv"
        # ]
        # args = parser.parse_args(generate_command)
        # args.func = autograder
        # args.func(args)

        # # first unzip and check output
        # os.mkdir(TEST_FILES_PATH + "autograder")
        # unzip_command = ["unzip", "-o", TEST_FILES_PATH + "autograder.zip", "-d", TEST_FILES_PATH + "autograder/source"]
        # unzip = subprocess.run(unzip_command, stdout=PIPE, stderr=PIPE)
        # self.assertEqual(len(unzip.stderr), 0, unzip.stderr.decode("utf-8"))

        # self.config["autograder_dir"] = TEST_FILES_PATH + "autograder"

        # # copy submission tests and notebook, 
        # os.mkdir(TEST_FILES_PATH + "autograder/submission")
        # os.mkdir(TEST_FILES_PATH + "autograder/results")
        # copyfile(TEST_FILES_PATH + "fails2and6H.ipynb", TEST_FILES_PATH + "autograder/submission/fails2and6H.ipynb")

        run_autograder(self.config['autograder_dir'])

        with open(TEST_FILES_PATH + "autograder/results/results.json") as f:
            actual_results = json.load(f)

        self.assertEqual(actual_results, self.expected_results, f"Actual results did not matched expected:\n{actual_results}")

        # self.assertDirsEqual(TEST_FILES_PATH + "autograder", TEST_FILES_PATH + "autograder-correct", ignore_ext=[".pdf",".zip"], ignore_dirs=["__pycache__"])

    def tearDown(self):
        self.deletePaths([
            TEST_FILES_PATH + "autograder/results/results.json",
            TEST_FILES_PATH + "autograder/__init__.py",
            TEST_FILES_PATH + "autograder/submission/test",
            TEST_FILES_PATH + "autograder/submission/tests",
            TEST_FILES_PATH + "autograder/submission/__init__.py",
        ])
