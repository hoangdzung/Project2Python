import MySQLdb
import time

def predictUserLoad (userID):
  # A test to see if the user alreadt exists in the Prediction table
  cursor = db.cursor()
  sqlSelectUser = ("SELECT UID FROM PREDICTION WHERE UID = %s", [userID])
  userExists = cursor.execute(*sqlSelectUser)
  cursor.close()

  # Get the monitored data for the user from the user monitor table
  cursor = db.cursor()
  sqlSelect = ("SELECT MAX(CPU), MAX(RAM), AVG(CPU), AVG(RAM), "\
    "MAX(RUN_TIME) FROM jSAMPLE WHERE UID = %s", [userID])
  cursor.execute(*sqlSelect)
  maxCPU, maxRAM, avgCPU, avgRAM, runTime = cursor.fetchone()
  cursor.close()

  # Get the user name and which server the user was last logged into
  cursor = db.cursor()
  sqlSelect = ("SELECT NAME, SERVER FROM USER WHERE UID = %s", [userID])
  cursor.execute(*sqlSelect)
  name, server = cursor.fetchone()
  cursor.close()

  # If the user doesn't exist we insert the new user with the data from the
  # user monitor table
  cursor = db.cursor()
  if userExists == 0:
    sqlInsert = ("INSERT INTO PREDICTION (UID, USER_NAME, LAST_USED_SERVER,"\
      " LAST_LOGIN, AVG_CPU, MAX_CPU, AVG_RAM, MAX_RAM) VALUES "\
      "(%s, %s, %s, %s, %s, %s, %s, %s)",
      (userID, name, server, runTime, avgCPU, maxCPU, avgRAM, maxRAM))
    cursor.execute(*sqlInsert)
    # If the user already exist in the prediction table we combine the existing
    # data with the new monitored data
  else:
    sqlSelect = ("SELECT AVG_CPU, MAX_CPU, AVG_RAM, MAX_RAM FROM PREDICTION"\
      " WHERE UID = %s", [userID])
    cursor.execute(*sqlSelect)
    preAvgCPU, preMaxCPU, preAvgRAM, preMaxRAM = cursor.fetchone()

    # Adjust the value of average CPU for the user in the prediction table by
    # using an algorithm adjusting the value based on the difference
    difference = avgCPU - preAvgCPU
    # newAvgCPU = changeAlgorithm(avgCPU, preAvgCPU, difference)
    newAvgCPU = (avgCPU + preAvgCPU) / 2

    # Same things for RAM
    difference = avgRAM - preAvgRAM
    # newAvgRAM = changeAlgorithm(avgRAM, preAvgRAM, difference)
    newAvgRAM = (avgRAM + preAvgRAM) / 2

    # Check if the user have heavier CPU jobs running in the system
    if maxCPU > preMaxCPU:
      newMaxCPU = maxCPU
    else:
      newMaxCPU = preMaxCPU

    # Same things for RAM
    if maxRAM > preMaxRAM:
      newMaxRAM = maxRAM
    else:
      newMaxRAM = preMaxRAM
    # Update the prediction table with the new calculated datta
    sqlInsert = ("UPDATE PREDICTION SET LAST_USED_SERVER = %s, LAST_LOGIN = %s,"\
      " AVG_CPU = %s, MAX_CPU = %s, AVG_RAM = %s, MAX_RAM = %s WHERE UID = %s",
      (server, runTime, newAvgCPU, newMaxCPU, newAvgRAM, newMaxRAM, userID))
    cursor.execute(*sqlInsert)
    # Clean up the user monitor table
  sqlDelete = ("DELETE FROM jSAMPLE WHERE UID = %s AND RUN_TIME <= %s",
    (userID, runTime))
  cursor.execute(*sqlDelete)
  cursor.close()
  db.commit()

def connect_database(name):
  global db
  try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="thanhdat97",
      db=name)
  except Exception, e:
    print(1, repr(e))

def get_db():
  return db

def run(db_name):
  connect_database(db_name)
  while(True):
    cursor = db.cursor()
    cursor.execute("SELECT UID FROM USER")

    for uid in cursor:
      predictUserLoad(uid[0])
    cursor.close()
    time.sleep(3600)

if __name__ == '__main__':
  run("MONITOR")
