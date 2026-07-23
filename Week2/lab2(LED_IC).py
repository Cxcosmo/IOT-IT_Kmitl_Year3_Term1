import time
import spidev
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ledpin = 18

GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)
pi_pwm.start(0)

spi = spidev.SpiDev() # Open SPI bus
spi.open(0, 0)
spi.max_speed_hz = 500000

def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

while True:
    reading = ReadChannel(0)
    percent = reading * 100 / 4096
    pi_pwm.ChangeDutyCycle(percent)
    time.sleep(0.05)
