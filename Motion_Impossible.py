#!/usr/bin/python

import MPU6050
import math
import time
import numpy

TargetSampleNumber = 10000
TargetRate =  1000
#Frequency =  8000 / ( integr value + 1)  minimum frequency=32,25

#InputSampleRate=raw_input("Sample Rate(32.25 ... 2000) ?")
#InputSampleNumber=raw_input("Number of sample to take ?")    

#TargetSampleNumber= int(InputSampleNumber)
#TargetRate= float(InputSampleRate)

mpu6050 = MPU6050.MPU6050()

mpu6050.setup()
mpu6050.setGResolution(2)
mpu6050.setSampleRate(TargetRate)
mpu6050.enableFifo(False)
time.sleep(0.01)

print "Capturing {0} samples at {1} samples/sec".format(TargetSampleNumber, mpu6050.SampleRate)

raw_input("Press enter to start")

mpu6050.resetFifo()
mpu6050.enableFifo(True)
time.sleep(0.01)

Values = []
Total = 0

while True:


 if mpu6050.fifoCount == 0:
     Status= mpu6050.readStatus()

     # print "Status",Status
     if (Status & 0x10) == 0x10 :
        print "Overrun Error! Quitting.\n"
        quit()

     if (Status & 0x01) == 0x01:
        Values.extend(mpu6050.readDataFromFifo())
 
 else:
        Values.extend(mpu6050.readDataFromFifo())

 #read Total number of data taken
 Total = len(Values)/14
 # print Total
 if Total >= TargetSampleNumber :
   break;

 #now that we have the data let's write the files


if Total > 0:
  Status = mpu6050.readStatus()
  # print "Status",Status
  if (Status & 0x10) == 0x10 :
    print "Overrun Error! Quitting.\n"
    quit()

  print "Saving RawData.txt  file."
  
  FO = open("RawData.txt","w")
  FO.write("Gx\tGy\tGz\tGyrox\tGyroy\tGyroz\n")

  for loop in range (TargetSampleNumber):
    SimpleSample = Values[loop*14 : loop*14+14]
    I = mpu6050.convertData(SimpleSample)
    FO.write("{0:6.3f}\t{1:6.3f}\t{2:6.3f}\t".format(I.Gx , I.Gy, I.Gz))
    FO.write("{0:6.3f}\t{1:6.3f}\t{2:6.3f}\n".format(I.Gyrox,I.Gyroy,I.Gyroz))

  FO.close()

print "Done!"
