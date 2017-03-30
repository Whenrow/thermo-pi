import os
import glob
import time
import sqlite3

# Module to load
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

# Min to pause
m = 10

# Start DB connection
conn = sqlite3.connect('temperatures.db')
c = conn.cursor()

# Getting the device file
w1_dir = '/sys/bus/w1/devices/'
thermFile = glob.glob(w1_dir + '28*')[0] + '/w1_slave'

# extract the temperature value
while True:
  with open(thermFile) as f:
    line = f.readlines()
    accept = line[0].split(' ')[-1]
    if (accept[0:3] == 'YES'):
      # get the value
      tp = line[1].split(' ')[-1]
      d = str(float(tp[2:7])/1000.0)

      # write in the table
      querry = 'INSERT INTO RECORDS VALUES (current_timestamp,'
      querry += str(d)
      querry += ',\'D1\');'
      print(querry)
      c.execute(querry)
      # Save (commit) the changes on the DB
      conn.commit()
    time.sleep(60*m)


# We close the connection if we are done with it.
conn.close()
