# -----------------------------------------------------------
# Device      : Raspberry-Pi 3 B+ (2018 Release)
# File name   : pir-led-light-bulb.py
# Description : Raspberry-Pi 3 B+ project. Motion detection LEDs & Light-Bulb.
# Author      : Kudzai Sean Huni
# E-mail      : kudzai@bcs.org

# -----------------------------------------------------------
# Website     : www.kudzai.xyz
# Date        : 19-05-2018
# -----------------------------------------------------------

# -----------------------------------------------------------
# Hardware:
#   1. Green LED
#   2. Red LED
#   3. Pir Motion Sensor
#   4. GPIO Expansion Board
#   5. GPIO Bread Board
#   6. 8-Channel Relay Module
#   7. Reading-Lamp/Light-Bulb (240 Volts)
# -----------------------------------------------------------

import RPi.GPIO as GPIO
import time
import collections as coll

freqs = coll.Counter()  # Declaring the Counter

lBulb = 22  # GPIO.BOARD=15 OR GPIO.BCM=22
pir = 16
redLed = 13
greenLed = 5

# Timers
lbTimerONN = 3.5
lbTimerOFF = 0.5

txtOnMotion = "Motion Detected !!!"
txtOnIdle = "System Idle..."
txtBulbONN = "Light-Bulb ONN..."
txtBulbOFF = "Light-Bulb OFF..."

GPIO.setmode(GPIO.BCM)  # Pin-Numbers by Broadcom SOC Channel


# Setting up/initiasing program parameters
def init():
    # Light & Motion Sensor Setup
    GPIO.setup(lBulb, GPIO.OUT)  # Relay Module Channel 1
    GPIO.setup(redLed, GPIO.OUT)  # Red LED
    GPIO.setup(greenLed, GPIO.OUT)  # Green LED
    GPIO.setup(pir, GPIO.IN)  # Motion Sesnor Input Expected

    GPIO.output(lBulb, GPIO.LOW)  # Turn off Chanel 1
    GPIO.output(redLed, GPIO.LOW)
    GPIO.output(greenLed, GPIO.HIGH)  # Turn onn LED


# Function Definition for cleaning-up environment.
def clear_up():
    GPIO.output(redLed, GPIO.LOW)
    GPIO.output(greenLed, GPIO.LOW)
    GPIO.output(lBulb, GPIO.LOW)  # GREEN LED-OFF
    GPIO.cleanup()  # Release Hardware Resources


# Turn onn the Red-Led to indicate motion detection.
# Simultaneously turn off the Green-Led as the Light Bulb Turns ONN.
def on_motion():
    print(txtBulbONN)
    GPIO.output(redLed, GPIO.HIGH)
    GPIO.output(greenLed, GPIO.LOW)
    GPIO.output(lBulb, GPIO.LOW)
    print(txtOnMotion)


# Waiting for an event to occur on the Motion-Sensor
def on_idle():
    print(txtBulbOFF)
    GPIO.output(redLed, GPIO.LOW)
    GPIO.output(greenLed, GPIO.HIGH)
    GPIO.output(lBulb, GPIO.HIGH)
    print(txtOnIdle)


def prg_loop():
    i = 1
    while True:
        # Counter Feedback
        print("Cycle: " + str(i))

        # Read input from the Pir-Motion Sensor
        irp = GPIO.input(pir)

        if irp == 0:
            on_idle()
            time.sleep(lbTimerOFF)
        elif irp == 1:
            on_motion()
            time.sleep(lbTimerONN)
        i += 1  # Increment counter by 1


# Program execution begins here...
if __name__ == '__main__':
    print('Press Ctrl-C to terminate program...')
    print('Initialising...')
    init()
    print('Initialisation complete!!!')

    try:
        prg_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the flowing code will be  executed.
        print(" Oh Noo, looks like our fun has been cut-short!!!")
        clear_up()

