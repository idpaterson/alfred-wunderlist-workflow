#!/usr/bin/env python

import os
import sys
import glob
import subprocess

NORMAL = '\033[0m'
BOLD   = '\033[1m'

def run_test_file(path):
	"""
	Uses osascript to execute an AppleScript test, returning True if the
	test passes or False if it fails. If the user cancels the test, this
	function will return None.
	"""
	try:
		output = subprocess.check_output('osascript "%s"' % path, shell=True)
	except:
		return None

	if output.strip() == '1':
		return True
	else:
		return False


if __name__ == '__main__':
	# Parse specific tests from the command line
	tests = []
	for arg in sys.argv[1:]:
		if '.applescript' in arg:
			if os.path.exists(arg):
				tests.append(arg)
		else:
			test_id = arg.split(' ')[0]
			test = glob.glob('%s*.applescript' % test_id)
			if len(test) > 0:
				tests += test

	# Or just run all tests
	if len(tests) == 0:
		tests = glob.glob('*.applescript')

	# Run the tests
	pass_count = 0
	fail_count = 0

	for test in tests:
		print 'Test %s' % test[:-12]
		result = run_test_file(test)

		if result is None:
			print '%sTests were cancelled%s' % (BOLD, NORMAL)
			break
		elif result:
			print "\t%sPASS%s" % (BOLD, NORMAL)
			pass_count += 1
		else:
			print "\t%sFAIL%s" % (BOLD, NORMAL)
			fail_count += 1

	print 'Passed %d / %d tests' % (pass_count, pass_count + fail_count)

	result = 1

	if fail_count > 0:
		print '%sFailed %d test%s%s' % (BOLD, fail_count, 's' if fail_count > 1 else '', NORMAL)
		result = 1
	else:
		print '%sAll tests passed%s' % (BOLD, NORMAL)
		result = 0

	# Show all tasks that were added during these tests
	subprocess.check_output('osascript "cleanup.applescript"', shell=True)

	sys.exit(result)
