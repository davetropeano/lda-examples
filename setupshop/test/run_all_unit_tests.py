import os
import glob
import unittest

test_file_strings = glob.glob('apitests/*.py')
module_strings = [str[0:len(str)-3] for str in [os.path.split(filestring)[1] for filestring in test_file_strings]]
test_file_strings = glob.glob('uitests/*.py')
module_strings = module_strings + [str[0:len(str)-3] for str in [os.path.split(filestring)[1] for filestring in test_file_strings]]
suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)