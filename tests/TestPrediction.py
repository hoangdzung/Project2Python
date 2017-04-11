import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import prediction as pr

class TestPrediction(unittest.TestCase):
  def test_run(self):
    print "Test prediction required run TestServerMonitor.py and TestUserMonitor.py first"
    pr.run("MONITOR_TEST")

if __name__ == '__main__':
  unittest.main()
