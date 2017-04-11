#Prototype of the load balancing algorith
import MySQLdb, MySQLdb.cursors
import sys
import datetime
import time

# Convert bytes to megabytes
def bytesToMegabytes(n):
  return (n / 1024) / 1024

# Check if the user already exists in the prediction table
def existingUser(userID):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT USER_NAME FROM PREDICTION WHERE"\
      " UID = %s", [userID])
    userExists = cursor.fetchone()
  except Exception, e:
    print 2, repr(e)

  cursor.close()
  if userExists == None:
    return False
  else:
    return True

# The last server user used
def lastUsedServer(userID):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT LAST_USED_SERVER, LAST_LOGIN"
      " FROM PREDICTION WHERE UID = %s", [userID])
    lastServer, lastLogin = cursor.fetchone()
  except Exception, e:
    print 2, repr(e)
  cursor.close()
  return lastServer, lastLogin

# the methods below use to check if cache available
def serverRAMload(server, timestamp):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT MIN(DISK_IN), MAX(DISK_IN) FROM"
      " sSAMPLE WHERE NAME = %s AND TIMESTAMP > %s", (server, timestamp))
    minDiskIn, maxDiskIn = cursor.fetchone()
  except Exception, e:
    print 2, repr(e)
  cursor.close()

  cursor = db.cursor()
  cachedRAM = 0
  try:
    cursor.execute("SELECT RAM_CACHED FROM sSAMPLE WHERE NAME = %s AND "
      "DISK_IN > %s", (server, maxDiskIn))
    cachedRAM = cursor.fetchone()[0]
  except Exception, e:
    print 2, repr(e)
  cursor.close()

  if minDiskIn != None and maxDiskIn != None:
    diskDifference = maxDiskIn - minDiskIn
  else:
    diskDifference, cachedRAM = 0, 0
  return diskDifference, cachedRAM

def getUserAvgRAM(userID):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT AVG_RAM FROM PREDICTION WHERE UID = %s",
      [userID])
    avgRAM = cursor.fetchone()[0]
  except Exception, e:
    print 2, repr(e)
  cursor.close()
  return avgRAM

def calculateCache(serverLoad, userLoad, cache):
  serverLoad = bytesToMegabytes(serverLoad)
  cacheNotReplaced = cache - serverLoad
  if cacheNotReplaced > userLoad:
    return True
  else:
    return False

def cacheAvailable(userID, lastServer, lastLogin):
  loadSinceLast, cachedRAM = serverRAMload(lastServer, lastLogin)
  avgRAMusage = getUserAvgRAM(userID)
  available = calculateCache(loadSinceLast, avgRAMusage, cachedRAM)
  if available:
    return True
  else:
    return False

# the methods below use to check if cpu available
def getServerCPU(server):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT CPU, TIMESTAMP FROM sSAMPLE WHERE"
      " NAME = %s ORDER BY TIMESTAMP DESC", [server])
    serverCPU, timestamp = cursor.fetchone()
  except Exception, e:
    print 2, repr(e)
  cursor.close()
  lastHour = timestamp - datetime.timedelta(hours=1)
  cursor = db.cursor()
  userCPU = []
  try:
    cursor.execute("SELECT AVG_CPU FROM PREDICTION WHERE LAST_USED_SERVER"
      " = %s AND LAST_LOGIN > %s", (server, lastHour))
    for elm in cursor:
      userCPU.append(elm[0])
  except Exception, e:
    print 2, repr(e)
  cursor.close()
  if serverCPU > sum(userCPU):
    return serverCPU
  else:
    return sum(userCPU)

def getUserCPU(userID):
  cursor = db.cursor()
  try:
    cursor.execute("SELECT AVG_CPU FROM PREDICTION WHERE UID = %s", [userID])
    userCPU = cursor.fetchone()[0]
  except Exception, e:
    print 2, repr(e)
  cursor.close()
  if userCPU == None:
    return 0
  else:
    return userCPU

def availableCPU(userID, lastServer):
  serverCPU = getServerCPU(lastServer)
  userCPU = getUserCPU(userID)
  totalCPU = serverCPU + userCPU
  return totalCPU < 100

#
def leastLoadServer():
  cursor = db.cursor()
  serverList = []
  try:
    cursor.execute("SELECT NAME FROM SERVER")
    for i in cursor:
      serverList.append(i)
  except Exception, e:
    print 2, repr(e)

  serverDict = {}
  for server in serverList:
    cursor = db.cursor()
    cursor.execute("SELECT CPU, TIMESTAMP FROM sSAMPLE"
      " WHERE NAME = %s ORDER BY TIMESTAMP DESC", [server[0]])
    activeServerLoad, timestamp = cursor.fetchone()
    cursor.close()

    lastHour = timestamp - datetime.timedelta(hours=1)
    userLoad = []

    cursor = db.cursor()
    cursor.execute("SELECT AVG_CPU FROM PREDICTION WHERE LAST_USED_SERVER"
      " = %s AND LAST_LOGIN > %s", (server[0],  lastHour))
    for i in cursor:
      userLoad.append(i[0])
    cursor.close()

    totalServerLoad = activeServerLoad + sum(userLoad)
    serverDict[server] = totalServerLoad

  if serverDict != {}:
    return min(serverDict, key=serverDict.get)[0]

# helpers
def connect_database(name):
  try:
    global db
    db = MySQLdb.connect(host="localhost", user="root", passwd="thanhdat97",
      db=name, cursorclass=MySQLdb.cursors.SSCursor)
  except Exception, e:
    print 1, repr(e)

def get_db():
  return db

def run(userID):
  userExists = existingUser(userID)
  if userExists:
    lastServer, lastLogin = lastUsedServer(userID)
    if cacheAvailable(userID, lastServer, lastLogin):
      if availableCPU(userID, lastServer):
        return lastServer
      else:
        return leastLoadServer()
    else:
      return leastLoadServer()
  else:
    return leastLoadServer()

if __name__== '__main__':
  connect_database("MONITOR")
  userID = sys.argv[1]
  print run(userID)
