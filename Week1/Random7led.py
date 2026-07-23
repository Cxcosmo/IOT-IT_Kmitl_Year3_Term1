
import RPi.GPIO as GPIO
import time
import random

GPIO.setmode (GPIO.BCM)

Red = 17
Green = 27
Blue = 22

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)

while True:
	GPIO.output(Red, round(random.random()))
	GPIO.output(Blue, round(random.random()))
	GPIO.output(Green, round(random.random()))
	time.sleep(1)
