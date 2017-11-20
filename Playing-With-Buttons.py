#!/usr/bin/python
#Playing with some buttons
#This code is written and located at Alex Eames http://RasPi.tv  
#I have mad slight changes to the code as needed
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()
import time
GPIO.setmode(GPIO.BCM)

# GPIO 23 & 24 set up as inputs. One pulled up, the other down.  
# 23 will go to GND when button pressed and 24 will go to 3V3 (3.3V)  
# this enables us to demonstrate both rising and falling edge detection  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now we'll define the threaded callback function  
# this will run in another thread when our event is detected  
def my_callback(channel):
    lcd.clear()
    lcd.message("Falling edge\non port 24!")
    print ("Rising edge detected on port 24 - even though, in the main thread,")
    print ("we are still waiting for a falling edge - cool story bro?\n")
    print ("Make sure you have a button connected so that when pressed")
    print ("it will connect GPIO port 23 (pin 16) to GND (pin 6)\n")
    print ("You will also need a second button connected so that when pressed")
    print ("It will connect GPIO port 24 (pin 18) to 3V3 (pin 1)")
raw_input(lcd.message("Press Enter n>"))

# The GPIO.add_event_detect() line below set things up so that
# when a rising edge is detected on port 24, regardless of whatever
# else is happening in the program, the function "my_callback" will be run
# It will happen even while the program is waiting for
# a falling edge on the other button.

GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback, bouncetime = 200)
          
try:
    lcd.clear()
    lcd.message("Waiting \n Port 23")
    print "Waiting for falling edge on port 23"
    GPIO.wait_for_edge(23, GPIO.FALLING)
    lcd.clear()
    lcd.message("You did it bro")
    print "Falling edge detected."
    
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
GPIO.cleanup() # clean up GPIO on normal exit
