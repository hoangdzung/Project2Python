from __future__ import division
import os, datetime, psutil, time, subprocess
import socket
import MySQLdb, MySQLdb.cursors
import logging
import pprint
import math
from decimal import *
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sets import Set
import numpy as np
from itertools import groupby


def getAllUsers():
  cursor = db.cursor()
  data = []
  try:
    cursor.execute("SELECT NAME FROM USER")
  except Exception, e:
    print(3, repr(e))

  for row in cursor:
    data.append(row[0])
  cursor.close()
  return data

def getUserID(userID):
  row = []
  cursor = db.cursor()
  try:
    UID = cursor.execute("SELECT UID FROM USER WHERE NAME = %s", [userID])
    row = cursor.fetchone()
  except Exception, e:
    print(2, repr(e))
  cursor.close()
  if row:
    return row[0]
  else:
    return None

def getJobs(UID):
  cursor = db.cursor()
  data = []
  try:
    cursor.execute("SELECT PID, START_TIME, CMD_NAME FROM JOB WHERE UID = %s",
      [UID])
  except Exception, e:
    print(3, repr(e))
  for i in cursor:
    data.append(i)
  cursor.close()
  return data

def getJobData(uid):
  cursor = db.cursor()
  data = []
  try:
    cursor.execute("SELECT CPU, RUN_TIME FROM jSAMPLE WHERE UID = %s", [uid])
  except Exception, e:
    print(4, repr(e))
  for i in cursor:
    data.append(i)
  cursor.close()
  return data

def getServer(UID):
  try:
    server = db.query("SELECT SERVER FROM USER WHERE UID = %s", (UID))
  except Exception, e:
    print(5, repr(e))
  return server

def getServerData(server):
  try:
    db.query("SELECT * FROM sSAMPLE WHERE NAME = %s", (server))
    server_data = db.store_result()
  except Exception, e:
    print(5, repr(e))
  return server_data

def topFive(data):
  dict1 = dict()
  returnData = []
  for item in data:
    if item[2] in dict1:
      dict1[item[2]] = dict1[item[2]] + 1
    else:
      dict1[item[2]] = 1

  count = 0
  for w in sorted(dict1, key=dict1.get, reverse=True):
    if count <= 5:
      combine = str(w) + " " + str(dict1[w])
      returnData.append(combine)
    count +=1
  return returnData

def averageJobCPU(jobData):
  maxCPU = 0
  mySum = 0
  cpuTotal = []
  endTime = jobData[-1][1]
  startTime = jobData[0][1]
  CPUstart = jobData[0][0]

  dataPoints = len(jobData)
  timeDiff = int((endTime - startTime).total_seconds())

  if dataPoints < timeDiff:
    for row in jobData:
      if int((row[1]-startTime).total_seconds()) > 1:
        diff = int((row[1] - startTime).total_seconds()) - 1
        missingCPU = Decimal((CPUstart+row[0]) / 2 * diff) + row[0]
      else:
        missingCPU = row[0]

      cpuTotal.append(missingCPU)
      startTime = row[1]
      CPUstart = row[0]

    if row[0] > maxCPU:
      maxCPU = round(row[0], 3)
  else:
    for row in jobData:
      missingCPU = row[0]
      cpuTotal.append(missingCPU)
      if row[0] > maxCPU:
        maxCPU = round(row[0], 3)

  try:
    mySum = sum(cpuTotal) / timeDiff
  except Exception, e:
    pass

  if mySum == None or mySum == 0:
    return 0, timeDiff, maxCPU
  else:
    return mySum, timeDiff, maxCPU

def averageTotalCPU(avgCPU):
  if len(avgCPU) == 0:
    return 0
  return round(sum(avgCPU)/len(avgCPU), 2)

def averageTotalTime(runTime):
  if len(runTime) == 0:
    return 0
  return sum(runTime)/len(runTime)

def timeConverter(sec):
  m, s = divmod(sec, 60)
  h, m = divmod(m, 60)
  return h, m, s

def generateGraphs(userID, userName):
  jobNames = []
  data = getJobs(userID)
  for item in data:
    jobNames.append(item[2])
  uniqueJobs = Set(jobNames)

  for item in uniqueJobs:
    avgCPU = []
    length = 0
    fig, ax = plt.subplots()
    itemData = []
    for row in data:
      rowData = []
      if row[2] == item:
        jobData = getJobData(userID)
        CPU, diff, maxCPU = averageJobCPU(jobData)
        avgCPU.append(CPU)
        for CPU in jobData:
          rowData.append(round(CPU[0], 3))
        if len(jobData) > length:
          length = len(jobData)
        itemData.append(rowData)

      x = [sum(e)/len(e) for e in zip(*itemData)]

      y = []
      count = 0
      while count < len(x):
        y.append(count)
        count += 1

      plt.plot(x)
      plt.axis([0, len(x), 0, 100])
      plt.xlabel('Time in Seconds')
      plt.ylabel('% CPU')
      plt.title(userName + ' - ' + item + ' AvgCPU: ' +\
        str(averageTotalCPU(avgCPU)))
      plt.grid(True)

  directory = 'trends/' + userName + '/'

  if not os.path.exists(directory):
    os.makedirs(directory)
  plt.savefig(directory + item + '.png')

def keyfunc(timestamp, interval = 60):
  # define a key function
  # 1. parse the datetime string to datetime object
  # 2. count the time delta (seconds)
  # 3. divided the time delta with interval, which is (6*60) here
  xt = datetime.datetime(2015, 4, 3)
  dt = datetime.datetime.strptime(timestamp.strftime('%d/%m/%Y %H:%M:%S'),
    '%d/%m/%Y %H:%M:%S')
  delta_second = int((dt-xt).total_seconds())
  normalize_second = (delta_second / interval) * interval
  return xt + datetime.timedelta(seconds=normalize_second)


def connect_database(name):
  global db
  try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="thanhdat97",
      db=name, cursorclass=MySQLdb.cursors.SSCursor)
  except Exception, e:
    print(1, repr(e))

def get_db():
  return db

def run(db_name):
  connect_database(db_name)
  logging.basicConfig(level=logging.DEBUG,
    filename='home/dsunde/master/dataPoints.log')

  userNames = getAllUsers()
  for userName in userNames:
    userID = getUserID(userName)
    generateGraphs(userID, userName)

    data = getJobData(userID)
    results = []
    for k, g in groupby(data, key=lambda i: keyfunc(i[1])):
      # k would be time interval "03/04/2013 13:30:00", "03/04/2013 13:35:00"
      # g would be the level, timestamp pair belong to the interval
      length = sum([1 for x in g])
      if length != 0:
        avg_level = sum([x[0] for x in g]) / length
      else:
        avg_level = 0
      results.append((k, avg_level))
    # print('results', results)

if __name__ == '__main__':
  run("MONITOR")
