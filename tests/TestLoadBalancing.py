import unittest
import data_test_lb as data
import random

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import loadBalancing as lb

class TestLoadBalancing(unittest.TestCase):
  def setUp(self):
    lb.connect_database("MONITOR_TEST")
    self.__cleanUpDatabase()
    self.__fakeData()

  def test_user_not_exist(self):
    # must forward to least load server
    uid = 5
    self.assertFalse(lb.existingUser(5))
    self.assertEqual(lb.run(uid), data.results["user_not_exist"])

  def test_user_exist_cache_false(self):
    # cache - serverLoad <= 20 (avg_ram in table PREDICTION with uid = 2)
    # must forward to least load server
    uid = 2
    self.assertTrue(lb.existingUser(2))
    lastServer, lastLogin = lb.lastUsedServer(uid)
    self.assertFalse(lb.cacheAvailable(uid, lastServer, lastLogin))
    self.assertEqual(lb.run(uid), data.results["user_exist_cache_false"])

  def test_user_exist_cache_true_availableCPU_false(self):
    # cache - serverLoad > 20 (avg_ram in table PREDICTION with uid = 3)
    # totalCPU = serverCPU + userCPU > 100
    # must forward to least load server
    uid = 3
    self.assertTrue(lb.existingUser(3))
    lastServer, lastLogin = lb.lastUsedServer(uid)
    self.assertTrue(lb.cacheAvailable(uid, lastServer, lastLogin))
    self.assertFalse(lb.availableCPU(uid, lastServer))
    self.assertEqual(lb.run(uid),
      data.results["user_exist_cache_true_availableCPU_false"])

  def test_user_exist_cache_true_availableCPU_true(self):
    # cache - serverLoad > 20 (avg_ram in table PREDICTION with uid = 4)
    # totalCPU = serverCPU + userCPU <= 100
    # must forward to last used server
    uid = 4
    self.assertTrue(lb.existingUser(4))
    self.assertTrue(lb.existingUser(3))
    lastServer, lastLogin = lb.lastUsedServer(uid)
    self.assertTrue(lb.cacheAvailable(uid, lastServer, lastLogin))
    self.assertTrue(lb.availableCPU(uid, lastServer))
    self.assertEqual(lb.run(uid),
      data.results["user_exist_cache_true_availableCPU_true"])


  @classmethod
  def __cleanUpDatabase(self):
    cursor = lb.get_db().cursor()
    cursor.execute("delete from jSAMPLE")
    cursor.execute("delete from JOB")
    cursor.execute("delete from sSAMPLE")
    cursor.execute("delete from PREDICTION")
    cursor.execute("delete from USER")
    cursor.execute("delete from SERVER")
    lb.get_db().commit()
    cursor.close()

  @classmethod
  def __fakeData(self):
    self.__addServer()
    self.__addSSample()
    self.__addUser()
    self.__addPrediction()
    lb.get_db().commit()

  @classmethod
  def __addServer(self):
    cursor = lb.get_db().cursor()
    for server_name in data.servers:
      cursor.execute("insert into SERVER (NAME) values (%s)", [server_name])
    cursor.close()

  @classmethod
  def __addSSample(self):
    cursor = lb.get_db().cursor()
    rs = data.random_ssamples
    for ss in data.ssamples:
      for timestamp in rs['timestamps']:
        string = "insert into sSAMPLE (NAME, TIMESTAMP, CPU, RAM, "\
          "RAM_AVAILABLE, RAM_CACHED, DISK_IN, DISK_OUT) values "\
          "(%s, %s, %s, %s, %s, %s, %s, %s)"
        args = (
          ss['name'],
          timestamp,
          random.uniform(rs['cpu']['from'], rs['cpu']['to']),
          random.uniform(rs['ram']['from'], rs['ram']['to']),
          random.randrange(rs['ram_available']['from'], rs['ram_available']['to']),
          random.randrange(rs['ram_cached']['from'], rs['ram_cached']['to']),
          random.randrange(rs['disk_in']['from'], rs['disk_in']['to']),
          random.randrange(rs['disk_out']['from'], rs['disk_out']['to'])
        )
        cursor.execute(string, args)

      cursor.execute("insert into sSAMPLE (NAME, TIMESTAMP, CPU, RAM, "
        "RAM_AVAILABLE, RAM_CACHED, DISK_IN, DISK_OUT) values "
        "(%s, %s, %s, %s, %s, %s, %s, %s)", (ss['name'], ss['timestamp'],
        ss['cpu'], ss['ram'], ss['ram_available'], ss['ram_cached'],
        ss['disk_in'], ss['disk_out']))
    cursor.close()

  @classmethod
  def __addUser(self):
    cursor = lb.get_db().cursor()
    for user in data.users:
      cursor.execute("insert into USER (UID, NAME, SERVER) values (%s, %s, %s)",
        (user['uid'], user['name'], user['server']))
    cursor.close()

  @classmethod
  def __addPrediction(self):
    cursor = lb.get_db().cursor()
    for pr in data.predictions:
      cursor.execute("insert into PREDICTION (UID, USER_NAME, LAST_USED_SERVER, "
        "LAST_LOGIN, AVG_CPU, MAX_CPU, AVG_RAM, MAX_RAM) values (%s, %s, %s, %s, "
        "%s, %s, %s, %s)", (pr['uid'], pr['user_name'], pr['last_used_server'],
        pr['last_login'], pr['avg_cpu'], pr['max_cpu'], pr['avg_ram'], pr['max_ram']))
    cursor.close()

if __name__ == '__main__':
  unittest.main()
