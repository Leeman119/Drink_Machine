#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import sys
import time
import threading

testing = True

hat1 = Adafruit_MotorHAT(addr=0x61)
hat2 = Adafruit_MotorHAT(addr=0x71)
hat3 = Adafruit_MotorHAT(addr=0x69)


class Pumps(Adafruit_MotorHAT):
    def __init__(self):

        self.number = int
        self.booze = str
        self.flavor = str
        self.brand = str
        self.bottle_size = float
        self.oz_left = float
        self.oneoz_timing = float
        self.reverse_pump = False
        self.speed = 255
        self.pump = object

    def pour(self, amount):
        self.pump.setSpeed(self.speed)
        if self.reverse_pump == 'True':
            # print 'Pouring ' + str(self.booze)
            print('Pouring ' + str(self.booze))
            if testing is not True:
                self.pump.run(Adafruit_MotorHAT.BACKWARD)
        else:
            # print 'Pouring ' + str(self.booze)
            print('Pouring ' + str(self.booze))
            if testing is not True:
                self.pump.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(self.oneoz_timing * amount)
        # print 'Stopping ' + str(self.booze)
        print('Stopping ' + str(self.booze))
        if testing is not True:
            self.pump.run(Adafruit_MotorHAT.RELEASE)

    def start(self):
        self.pump.setSpeed(self.speed)
        if self.reverse_pump == 'True':
            # print 'Pouring ' + str(self.booze)
            print('Pouring ' + str(self.booze))
            if testing is not True:
                self.pump.run(Adafruit_MotorHAT.BACKWARD)
        else:
            # print 'Pouring ' + str(self.booze)
            print('Pouring ' + str(self.booze))
            if testing is not True:
                self.pump.run(Adafruit_MotorHAT.FORWARD)

    def stop(self):
        # print 'Stopping ' + str(self.booze)
        print('Stopping ' + str(self.booze))
        if testing is not True:
            self.pump.run(Adafruit_MotorHAT.RELEASE)

    
    
