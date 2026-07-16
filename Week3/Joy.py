import time
import spidev
import RPi.GPIO as GPIO

# ---------- ตั้งค่า SPI สำหรับ MCP3208 ----------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# ---------- ตั้งค่า GPIO สำหรับขา SW ----------
SW_PIN = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ReadChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def adc_to_percent(reading):
    return (reading * 100) / 4095

try:
    while True:
        vrx = ReadChannel(0)
        vry = ReadChannel(1)
        sw_state = GPIO.input(SW_PIN)

        x_percent = adc_to_percent(vrx)
        y_percent = adc_to_percent(vry)
        sw_status = "PRESSED" if sw_state == 0 else "released"

        print("VRx=%d (%.1f%%)\t VRy=%d (%.1f%%)\t SW=%s" %
              (vrx, x_percent, vry, y_percent, sw_status))

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStop")

finally:
    GPIO.cleanup()
    spi.close()
