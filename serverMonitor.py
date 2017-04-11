import psutil
import socket
import pwd, os, time
import subprocess
import MySQLdb
import logging

def bytesToMegabytes(n):
  return (n / 1024) / 1024

def getCPU():
  numOfCPU = psutil.cpu_count()
  usageCPU = psutil.cpu_percent()
  currentUsage = usageCPU / numOfCPU
  return round(usageCPU, 3)

def getIO():
  read_count, write_count, read_bytes, write_bytes, read_time, write_time\
    = psutil.disk_io_counters()[:6]
  return read_bytes, write_bytes

def getRAM() :
  tot, available, percent, used, free, active, inactive, buff, cache\
    = psutil.virtual_memory()[:9]
  return round(percent, 3), bytesToMegabytes(available),\
    bytesToMegabytes(cache)

def updateServer():
  cpu = getCPU()
  read_count, write_count = getIO()
  ram, available, cache = getRAM()
  cursor = db.cursor()
  try:
    server = cursor.execute("SELECT NAME FROM SERVER WHERE NAME = %s ",
      [hostname])
  except Exception, e:
    print 2, repr(e)

  if server == 0:
    try:
      cursor.execute("INSERT INTO SERVER (NAME) VALUES (%s) ", [hostname])
    except Exception, e:
      print 3, repr(e)

  try:
    cursor.execute("INSERT INTO sSAMPLE (NAME, CPU, RAM, RAM_AVAILABLE,"\
      " RAM_CACHED, DISK_IN, DISK_OUT) VALUES (%s, %s, %s, %s, %s,"\
      " %s, %s) ", (hostname, cpu, ram, available, cache, read_count,
      write_count))
  except Exception, e:
    print 4, repr(e)
  cursor.close()
  db.commit()

def get_db():
  return db

def get_hostname():
  return hostname

def connect_database(name):
  try:
    global db
    db = MySQLdb.connect(host="10.0.2.2", user="root", passwd="thanhdat97",
      db=name)
  except Exception, e:
    print 1,repr(e)

def init_hostname():
  global hostname
  hostname = socket.gethostname()

def run(db_name):
  logging.basicConfig(level=logging.DEBUG,
    filename='home/dsunde/master/server.log')

  connect_database(db_name)
  init_hostname()

  while(True):
    try:
      updateServer()
    except:
      logging.exception("Error : ")
    time.sleep(60)

if __name__ == '__main__':
  run("MONITOR")
