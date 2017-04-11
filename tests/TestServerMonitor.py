import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import serverMonitor as sm

class TestServer(unittest.TestCase):
  def test_bytesToMegabytes(self):
    self.assertEqual(0, sm.bytesToMegabytes(1024))
    self.assertEqual(1, sm.bytesToMegabytes(1024*1024))

  def test_run(self):
    sm.run("MONITOR_TEST")

if __name__ == '__main__':
  unittest.main()
