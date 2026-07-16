
import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)

Red = 17
Green = 27
Blue = 22

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)

while True:
	GPIO.output(Red, False)
	GPIO.output(Blue, False)
	GPIO.output(Green, True)
	time.sleep(1)
	GPIO.output(Red, True)
	GPIO.output(Blue, False)
	GPIO.output(Green, False)
	time.sleep(1)
	GPIO.output(Red, True)
	GPIO.output(Blue, False)
	GPIO.output(Green, True)
	time.sleep(1)
	GPIO.output(Red, True)
	GPIO.output(Green, False)
	GPIO.output(Blue, True)
	time.sleep(1)
	GPIO.output(Red, False)
	GPIO.output(Green, False)
	GPIO.output(Blue, True)
	time.sleep(1)
	GPIO.output(Red, False)
	GPIO.output(Green, True)
	GPIO.output(Blue, True)
	time.sleep(1)
	GPIO.output(Red, False)
	GPIO.output(Green, False)
	GPIO.output(Blue, False)
