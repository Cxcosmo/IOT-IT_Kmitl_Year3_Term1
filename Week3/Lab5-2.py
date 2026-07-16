import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 2
ECHO = 3

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)  # ให้เซนเซอร์นิ่งก่อนยิงสัญญาณ

    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.04  # กันค้าง: timeout 40ms (ระยะไกลสุด ~4m นานสุด ~23ms)

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None  # ไม่มีสัญญาณตอบกลับ

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None  # สัญญาณค้าง

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)


try:
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    while True:
        distance = get_distance()
        if distance is not None and 2 <= distance <= 400:
            print("Distance:", distance, "cm")
        else:
            print("Out of range or no echo received")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nหยุดการทำงาน")

finally:
    GPIO.cleanup()
