#!/usr/bin/env python
# Joel Oliphant
# Analog Input with ACDC0832 chip
# Code Credit
# //heinrichhartmann.com/blog/2014/12/14/Sensor-Monitoring-with-RaspberryPi-and-Circonus.html
# Datasheet: http://www.ti.com/lit/ds/symlink/acdc0838-n.pdf
# Part of SunFounder LCD StarterKit
# http://www.sunfounder.com/index.php?c=show&id=21&model=LCD%20Starter%20Kit
# Code modified to add volts per bit and return a floating number

import time
import os
import RPi.GPIO as GPIO
import Adafruit_CharLCDPlate()
import subprocess

lcd = LCD.Adafruit_CharLCDPlate()

GPIO.setmode(GPIO.BCM)

# bits are for 3.3 input
Volt_Per_Bit = (3.3/255)

# SPI port on the ADC to the Cobbler
PIN_CLK = 18
PIN_DO = 27
PIN_DI = 22
PIN_CS = 17

# set up the SPI interface pins
GPIO.setup(PIN_DI, GPIO.OUT)
GPIO.setup(PIN_DO, GPIO.IN)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_CS, GPIO.OUT)

# read SPI data from ADC8032
def getADC(channel):
    # 1. CS LOW
    GPIO.output(PIN_CS, True)
    GPIO.output(PIN_CS, False)

    # 2. Start clock
    GPIO.output(PIN_CLK, False)

    # 3. Input MUX address
    for i in [1,1,channel]: # start bit + mux assignment
        if (i == 1):
            GPIO.output(PIN_DI, True)
        else:
            GPIO.output(PIN_DI, False)

        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)

    # 4. read 8 ADC bits
    ad = 0
    for i in range(8):
        GPIO.output(PIN_CLK, True)
        GPIO.output(PIN_CLK, False)
        ad <<= 1
        if (GPIO.input(PIN_DO)):
            ad |= 0x1

    # 5. reset
    GPIO.output(PIN_CS, True)

    return ad * Volt_Per_Bit

if_name_ == "_main_":
    while True:
        print "ADC[0]: {}\t ADC[1]: {}".format(getADC(0), getADC(1))

        Output_String = "ADC[0]: %.3f \t ADC[1]: %.3f" %(getADC(0), getADC(1))

        time.sleep(1)
        lcd.message(Output_String)
        time.sleep(2)
        lcd.clear()
        continue



