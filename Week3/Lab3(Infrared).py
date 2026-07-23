import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

EN = 2
OUT = 3

GPIO.setup(EN, GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

GPIO.output(EN, GPIO.HIGH)
time.sleep(0.1)

count = 0
print(f"Count = {count}") 
previous_input = GPIO.input(OUT)

while True:
    current_input = GPIO.input(OUT)
    if current_input != previous_input and not current_input:
        count += 1
        print(f"Count = {count}")
    previous_input = current_input
    time.sleep(0.1)
